# coding: utf-8

# 使用linux命令虚拟机磁盘，然后返回根目录下的文件的访问控制权限


def list_access_controll(args):
    import os
    mod_path = os.getcwd() + '/access_detection/nbd.ko'

    os.system('insmod ' + mod_path + ' max_part=16')
    os.system('qemu-nbd -c /dev/nbd0 ' + args['path'])
    os.system('mount /dev/nbd0p1 /mnt')
    result = os.system('ls -lh /mnt')
    os.system('umount /mnt')
    os.system('qemu-nbd --disconnect /dev/nbd0')
    print result
    return result