# Code derived from https://github.com/pytorch/examples/blob/master/imagenet/main.py

import argparse
import os
import random
import shutil
import time
import warnings
import subprocess

import torch
import torch.nn as nn
import torch.nn.parallel
import torch.backends.cudnn as cudnn
import torch.distributed as dist
import torch.optim
import torch.utils.data
import torch.utils.data.distributed
import torchvision.transforms as transforms
import torchvision.datasets as datasets
import torchvision.models as models

model_names = sorted(name for name in models.__dict__
    if name.islower() and not name.startswith("__")
    and callable(models.__dict__[name]))

parser = argparse.ArgumentParser(description='PyTorch ImageNet Training')
parser.add_argument('data', metavar='DIR',
                    help='path to dataset')
parser.add_argument('--arch', '-a', metavar='ARCH', default='resnet18',
                    choices=model_names,
                    help='model architecture: ' +
                        ' | '.join(model_names) +
                        ' (default: resnet18)')
parser.add_argument('-j', '--workers', default=4, type=int, metavar='N',
                    help='number of data loading workers (default: 4)')
parser.add_argument('--epochs', default=1, type=int, metavar='N',
                    help='number of total epochs to run')
parser.add_argument('--start-epoch', default=0, type=int, metavar='N',
                    help='manual epoch number (useful on restarts)')
parser.add_argument('-b', '--batch-size', default=256, type=int,
                    metavar='N', help='mini-batch size (default: 256)')
parser.add_argument('--lr', '--learning-rate', default=0.1, type=float,
                    metavar='LR', help='initial learning rate')
parser.add_argument('--momentum', default=0.9, type=float, metavar='M',
                    help='momentum')
parser.add_argument('--weight-decay', '--wd', default=1e-4, type=float,
                    metavar='W', help='weight decay (default: 1e-4)')
parser.add_argument('--print-freq', '-p', default=1000, type=int,
                    metavar='N', help='print frequency (default: 1000)')
parser.add_argument('--resume', default='', type=str, metavar='PATH',
                    help='path to latest checkpoint (default: none)')
parser.add_argument('-e', '--evaluate', dest='evaluate', action='store_true',
                    help='evaluate model on validation set')
parser.add_argument('--pretrained', dest='pretrained', action='store_true',
                    help='use pre-trained model')
parser.add_argument('--world-size', default=1, type=int,
                    help='number of distributed processes')
parser.add_argument('--dist-url', default='tcp://224.66.41.62:23456', type=str,
                    help='url used to set up distributed training')
parser.add_argument('--dist-backend', default='gloo', type=str,
                    help='distributed backend')
parser.add_argument('--seed', default=None, type=int,
                    help='seed for initializing training. ')
parser.add_argument('--gpu', default=None, type=int,
                    help='GPU id to use.')
parser.add_argument('--run', default='1', type=str,
                    help='Run number or run info that defines the result dir.')
parser.add_argument('--numGPUs', default=None, type=int, metavar='N',
                    help='Number of GPUs to use')
parser.add_argument('--mode', default='Run', type=str,
                    help='What mode is the code running.')
parser.add_argument('--break-point', default=1, type=int,
                    metavar='N', help='batch size (default: 1) to test')
best_acc1 = 0


GPUs = {1: '0', 2:'0,1', 3:'0,1,2', 4:'0,1,2,3'}

def main():
    global args, best_acc1, result_dir, GPUs
    args = parser.parse_args()
    result_dir = "results/run-"
    start_prgm = time.time()
    if args.seed is not None:
        random.seed(args.seed)
        torch.manual_seed(args.seed)
        cudnn.deterministic = True
        warnings.warn('You have chosen to seed training. '
                      'This will turn on the CUDNN deterministic setting, '
                      'which can slow down your training considerably! '
                      'You may see unexpected behavior when restarting '
                      'from checkpoints.')

    if args.gpu is not None:
        warnings.warn('You have chosen a specific GPU. This will completely '
                      'disable data parallelism.')

    args.distributed = args.world_size > 1

    if args.distributed:
        dist.init_process_group(backend=args.dist_backend, init_method=args.dist_url,
                                world_size=args.world_size)
    
    if args.numGPUs:
        import os
        os.environ['CUDA_VISIBLE_DEVICES']=GPUs[args.numGPUs]
        print("CUDA VISIBLE DEVICES", os.environ['CUDA_VISIBLE_DEVICES'])

    # Create the result directory
    result_dir += args.run
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    #command = "top -b > "
    #command += result_dir + "/top-model.txt &"
    #subprocess.call(command, shell=True)
    #command = "iostat -d 1 -p sdb > "
    #command += result_dir + "/iostat-model.txt &"
    #subprocess.call(command, shell=True)
    #command = "sudo iotop -b > "
    #command += result_dir + "/iotop-model.txt &"
    #subprocess.call(command, shell=True)
    ##command = "sudo blktrace -d /dev/sdb -o - | blkparse -i - > "
    ##command += result_dir + "/blktrace-model.txt &"
    #command = "nvidia-smi -l 1  > "
    #command += result_dir + "/gpu-model.txt &"
    #subprocess.call(command, shell=True)

    # Let's print memory util before creating the model:
    print("\nMemory before model creation : ")
    subprocess.call("free -m", shell=True)

    # create model
    if args.pretrained:
        print("=> using pre-trained model '{}'".format(args.arch))
        model = models.__dict__[args.arch](pretrained=True)
    else:
        print("=> creating model '{}'".format(args.arch))
        model = models.__dict__[args.arch]()

    if args.gpu is not None:
        model = model.cuda(args.gpu)
    elif args.distributed:
        model.cuda()
        model = torch.nn.parallel.DistributedDataParallel(model)
    else:
        if args.arch.startswith('alexnet') or args.arch.startswith('vgg'):
            model.features = torch.nn.DataParallel(model.features)
            model.cuda()
        else:
            model = torch.nn.DataParallel(model).cuda()

    print("\nMemory after creating model : ")
    subprocess.call("free -m", shell=True)



    # define loss function (criterion) and optimizer
    criterion = nn.CrossEntropyLoss().cuda(args.gpu)

    optimizer = torch.optim.SGD(model.parameters(), args.lr,
                                momentum=args.momentum,
                                weight_decay=args.weight_decay)

    # optionally resume from a checkpoint
    if args.resume:
        if os.path.isfile(args.resume):
            print("=> loading checkpoint '{}'".format(args.resume))
            checkpoint = torch.load(args.resume)
            args.start_epoch = checkpoint['epoch']
            best_acc1 = checkpoint['best_acc1']
            model.load_state_dict(checkpoint['state_dict'])
            optimizer.load_state_dict(checkpoint['optimizer'])
            print("=> loaded checkpoint '{}' (epoch {})"
                  .format(args.resume, checkpoint['epoch']))
        else:
            print("=> no checkpoint found at '{}'".format(args.resume))

    cudnn.benchmark = True

    # Data loading code
    traindir = os.path.join(args.data, 'train')
    valdir = os.path.join(args.data, 'val')
    normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                     std=[0.229, 0.224, 0.225])

    train_dataset = datasets.ImageFolder(
        traindir,
        transforms.Compose([
            transforms.RandomResizedCrop(224),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            normalize,
        ]))

    if args.distributed:
        train_sampler = torch.utils.data.distributed.DistributedSampler(train_dataset)
    else:
        train_sampler = None

    train_loader = torch.utils.data.DataLoader(
        train_dataset, batch_size=args.batch_size, shuffle=(False),
        num_workers=args.workers, pin_memory=True, sampler=train_sampler)

    val_loader = torch.utils.data.DataLoader(
        datasets.ImageFolder(valdir, transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            normalize,
        ])),
        batch_size=args.batch_size, shuffle=False,
        num_workers=args.workers, pin_memory=True)

    if args.evaluate:
        validate(val_loader, model, criterion)
        return

    import sys
    print("TYPE OF DATASET: ", type(train_dataset), len(train_dataset), sys.getsizeof(train_dataset))
    print("TYPE of ith in DATASET: ", type(train_dataset[0]), train_dataset[0][0].element_size(), train_dataset[0][0].nelement(), sys.getsizeof(train_dataset[0][1]))
    #n = 1279867
    #print "TYPE of last in DATASET: ", type(train_dataset[n-1]), train_dataset[n-1][0].element_size(), train_dataset[n-1][0].nelement()
    1279867
    print(train_dataset[0])
    #sys.exit()

    #subprocess.call("sudo kill $(pgrep blk)", shell=True)
    subprocess.call("kill $(pgrep iostat)", shell=True)
    subprocess.call("sudo kill $(pgrep iotop)", shell=True)
    subprocess.call("kill $(pgrep top)", shell=True)
    subprocess.call("kill $(pgrep nvidia-smi)", shell=True)

    #subprocess.call("free -m", shell = True)
    #subprocess.call("echo 3 | sudo tee /proc/sys/vm/drop_caches", shell = True)
    #subprocess.call("free -m", shell = True)


    #command = "top -b > "
    #command += result_dir + "/top-train.txt &"
    #subprocess.call(command, shell=True)
    #command = "iostat -d 1 -p sdb > "
    #command += result_dir + "/iostat-train.txt &"
    #subprocess.call(command, shell=True)
    #command = "sudo iotop -b > "
    #command += result_dir + "/iotop-train.txt &"
    #subprocess.call(command, shell=True)
    #command = "nvidia-smi -l 1  > "
    #command += result_dir + "/gpu-train.txt &"
    #subprocess.call(command, shell=True)
    #command = "sudo blktrace -d /dev/sdb -o - | blkparse -i - > "
    #command += result_dir + "/blktrace-train.txt &"
    #subprocess.call(command, shell=True)
    
    for epoch in range(args.start_epoch, args.epochs):
        if args.distributed:
            train_sampler.set_epoch(epoch)
        adjust_learning_rate(optimizer, epoch)

        command = "top -b >> "
        command +=result_dir + "/top-train.txt &"
        subprocess.call(command, shell=True)
        command = "echo next epoch >> "
        command += result_dir + "/iostat-train.txt"
        subprocess.call(command, shell=True)
        command = "iostat -dx 1 -p /dev/sdb >> "
        command += result_dir + "/iostat-train.txt &"
        subprocess.call(command, shell=True)
        command = "sudo iotop -b >> "
        command += result_dir + "/iotop-train.txt &"
        subprocess.call(command, shell=True)
        command = "nvidia-smi -l 1  >> "
        command += result_dir + "/gpu-train.txt &"
        subprocess.call(command, shell=True)

        # train for one epoch
        start_epoch_time = time.time()
        print('Epoch ', epoch, ' starts at ', start_epoch_time)

        train(train_loader, model, criterion, optimizer, epoch)
        
        end_epoch_time = time.time()
        print('Epoch ', epoch, 'ends at', end_epoch_time)
        print('Total time taken by epoch ', end_epoch_time - start_epoch_time)
        
        subprocess.call("kill $(pgrep iostat)", shell=True)
        subprocess.call("sudo kill $(pgrep iotop)", shell=True)
        subprocess.call("kill $(pgrep top)", shell=True)
        subprocess.call("kill $(pgrep nvidia-smi)", shell=True)

        # evaluate on validation set
        #acc1 = validate(val_loader, model, criterion)

        # remember best acc@1 and save checkpoint
        #is_best = acc1 > best_acc1
        #best_acc1 = max(acc1, best_acc1)
        #save_checkpoint({
        #    'epoch': epoch + 1,
        #    'arch': args.arch,
        #    'state_dict': model.state_dict(),
        #    'best_acc1': best_acc1,
        #    'optimizer' : optimizer.state_dict(),
        #}, is_best)
        #print('Accuracy in the epoch: ',acc1)
        #if(best_acc1 > 72):
        #    print("best accuracy acheived", best_acc1)
        #    break;

    #subprocess.call("sudo kill $(pgrep blk)", shell=True)
    subprocess.call("kill $(pgrep iostat)", shell=True)
    subprocess.call("sudo kill $(pgrep iotop)", shell=True)
    subprocess.call("kill $(pgrep top)", shell=True)
    subprocess.call("kill $(pgrep nvidia-smi)", shell=True)
    
    end_prgm = time.time()
    print("\nTotal time taken : ", end_prgm - start_prgm)


def train(train_loader, model, criterion, optimizer, epoch):
    batch_time = AverageMeter()
    data_time = AverageMeter()
    to_gpu_time = AverageMeter()
    process_time = AverageMeter()
    losses = AverageMeter()
    top1 = AverageMeter()
    top5 = AverageMeter()

    # switch to train mode
    model.train()

    import psutil
    before_read_count = psutil.disk_io_counters(perdisk=True)['sdb'].read_count
    before_read_bytes = psutil.disk_io_counters(perdisk=True)['sdb'].read_bytes
    
    currentDevices = torch.cuda.device_count()
    print("CURRENT DEVICES ", currentDevices)

    start_for_loop = time.time()
    prev = start_for_loop
    for i, (input, target) in enumerate(train_loader):
        # measure data loading time
        end_for_loop = time.time()
        data_time.update(end_for_loop - prev)

        after_read_count = psutil.disk_io_counters(perdisk=True)['sdb'].read_count
        after_read_bytes = psutil.disk_io_counters(perdisk=True)['sdb'].read_bytes
        disk_io_count = after_read_count - before_read_count
        disk_io_bytes = after_read_bytes - before_read_bytes

        #gpuMaxUsage = torch.cuda.max_memory_allocated()
        #gpuMemUsage = torch.cuda.memory_allocated()
        #print("GPU MEMORY USAGE ", gpuMemUsage, gpuMaxUsage)

        #gpuMaxCache = torch.cuda.max_memory_cached()
        #gpuMemCache = torch.cuda.memory_cached()
        #print("GPU MEMORY CACHED ", gpuMemCache, gpuMaxCache)

        if args.gpu is not None:
            input = input.cuda(args.gpu, non_blocking=True)
        target = target.cuda(args.gpu, non_blocking=True)
        to_gpu_time.update(time.time() - end_for_loop)

        process_start = time.time()
        # compute output
        print("input size ", input.size(), input.nelement()*input.element_size())
        output = model(input)
        print("output size ", output.size(), output.nelement()*output.element_size())
        loss = criterion(output, target)
        
        # measure accuracy and record loss
        acc1, acc5 = accuracy(output, target, topk=(1, 5))
        losses.update(loss.item(), input.size(0))
        top1.update(acc1[0], input.size(0))
        top5.update(acc5[0], input.size(0))

        # compute gradient and do SGD step
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        process_time.update(time.time() - process_start)
        # measure elapsed time
        batch_time.update(time.time() - prev)

        if i % args.print_freq == 0:
            print('Epoch: [{0}][{1}/{2}]\t'
                  'DiskIO {3},{4}\t'
                  'BatchTime {batch_time.val:.6f} ({batch_time.avg:.6f})\t'
                  'DataTime {data_time.val:.6f} ({data_time.avg:.6f})\t'
                  'GPUProcessTime {process_time.val:.6f} ({process_time.avg:.6f})\t'
                  'GPU {to_gpu_time.val:.6f} ({to_gpu_time.avg:.6f})\t'.format(
                   epoch, i, len(train_loader), disk_io_count, disk_io_bytes, batch_time=batch_time,
                   data_time=data_time, process_time=process_time, to_gpu_time=to_gpu_time))

        if args.mode == 'Optimize':
            if  i == args.break_point:
                break;
        
        gpuMaxUsage = torch.cuda.max_memory_allocated()
        gpuMemUsage = torch.cuda.memory_allocated()
        print("GPU MEMORY USAGE ", gpuMemUsage, gpuMaxUsage)

        gpuMaxCache = torch.cuda.max_memory_cached()
        gpuMemCache = torch.cuda.memory_cached()
        print("GPU MEMORY CACHED ", gpuMemCache, gpuMaxCache)
        
        prev = time.time()
        #if i % args.print_freq == 0:
        #    print('Epoch: [{0}][{1}/{2}]\t'
        #          'DiskIO {3},{4}\t'
        #          'BatchTime {batch_time.val:.6f} ({batch_time.avg:.6f})\t'
        #          'DataTime {data_time.val:.6f} ({data_time.avg:.6f})\t'
        #          'GPU {to_gpu_time.val:.6f} ({to_gpu_time.avg:.6f})\t'
        #          'Loss {loss.val:.4f} ({loss.avg:.4f})\t'
        #          'Acc@1 {top1.val:.3f} ({top1.avg:.3f})\t'
        #          'Acc@5 {top5.val:.3f} ({top5.avg:.3f})'.format(
        #           epoch, i, len(train_loader), disk_io_count, disk_io_bytes, batch_time=batch_time,
        #           data_time=data_time, to_gpu_time=to_gpu_time, loss=losses, top1=top1, top5=top5))


def validate(val_loader, model, criterion):
    batch_time = AverageMeter()
    losses = AverageMeter()
    top1 = AverageMeter()
    top5 = AverageMeter()

    # switch to evaluate mode
    model.eval()

    with torch.no_grad():
        end = time.time()
        for i, (input, target) in enumerate(val_loader):
            if args.gpu is not None:
                input = input.cuda(args.gpu, non_blocking=True)
            target = target.cuda(args.gpu, non_blocking=True)

            # compute output
            output = model(input)
            loss = criterion(output, target)

            # measure accuracy and record loss
            acc1, acc5 = accuracy(output, target, topk=(1, 5))
            losses.update(loss.item(), input.size(0))
            top1.update(acc1[0], input.size(0))
            top5.update(acc5[0], input.size(0))

            # measure elapsed time
            batch_time.update(time.time() - end)
            end = time.time()

            if i % args.print_freq == 0:
                print('Test: [{0}/{1}]\t'
                      'Time {batch_time.val:.6f} ({batch_time.avg:.6f})\t'
                      'Loss {loss.val:.4f} ({loss.avg:.4f})\t'
                      'Acc@1 {top1.val:.3f} ({top1.avg:.3f})\t'
                      'Acc@5 {top5.val:.3f} ({top5.avg:.3f})'.format(
                       i, len(val_loader), batch_time=batch_time, loss=losses,
                       top1=top1, top5=top5))

        print(' * Acc@1 {top1.avg:.3f} Acc@5 {top5.avg:.3f}'
              .format(top1=top1, top5=top5))

    return top1.avg


def save_checkpoint(state, is_best, filename='checkpoint.pth.tar'):
    torch.save(state, filename)
    if is_best:
        shutil.copyfile(filename, 'model_best.pth.tar')


class AverageMeter(object):
    """Computes and stores the average and current value"""
    def __init__(self):
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count


def adjust_learning_rate(optimizer, epoch):
    """Sets the learning rate to the initial LR decayed by 10 every 30 epochs"""
    lr = args.lr * (0.1 ** (epoch // 30))
    for param_group in optimizer.param_groups:
        param_group['lr'] = lr


def accuracy(output, target, topk=(1,)):
    """Computes the accuracy over the k top predictions for the specified values of k"""
    with torch.no_grad():
        maxk = max(topk)
        batch_size = target.size(0)

        _, pred = output.topk(maxk, 1, True, True)
        pred = pred.t()
        correct = pred.eq(target.view(1, -1).expand_as(pred))

        res = []
        for k in topk:
            correct_k = correct[:k].view(-1).float().sum(0, keepdim=True)
            res.append(correct_k.mul_(100.0 / batch_size))
        return res


if __name__ == '__main__':
    main()

