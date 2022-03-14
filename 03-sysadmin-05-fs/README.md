# Домашнее задание к занятию "3.5. Файловые системы"

1. Узнайте о [sparse](https://ru.wikipedia.org/wiki/%D0%A0%D0%B0%D0%B7%D1%80%D0%B5%D0%B6%D1%91%D0%BD%D0%BD%D1%8B%D0%B9_%D1%84%D0%B0%D0%B9%D0%BB) (разряженных) файлах.
    ## Ответ
    Если правильно понял это способ сжатия файлов для экономии места
    
    ---
    
1. Могут ли файлы, являющиеся жесткой ссылкой на один объект, иметь разные права доступа и владельца? Почему?
    ## Ответ
    Не могут, увидел это еще на лекции, так как hardlink это ссылка на тот же самый файл и имеет тот же inode то права будут одни и теже
    
    ---
    
1. Сделайте `vagrant destroy` на имеющийся инстанс Ubuntu. Замените содержимое Vagrantfile следующим:

    ```bash
    Vagrant.configure("2") do |config|
      config.vm.box = "bento/ubuntu-20.04"
      config.vm.provider :virtualbox do |vb|
        lvm_experiments_disk0_path = "/tmp/lvm_experiments_disk0.vmdk"
        lvm_experiments_disk1_path = "/tmp/lvm_experiments_disk1.vmdk"
        vb.customize ['createmedium', '--filename', lvm_experiments_disk0_path, '--size', 2560]
        vb.customize ['createmedium', '--filename', lvm_experiments_disk1_path, '--size', 2560]
        vb.customize ['storageattach', :id, '--storagectl', 'SATA Controller', '--port', 1, '--device', 0, '--type', 'hdd', '--medium', lvm_experiments_disk0_path]
        vb.customize ['storageattach', :id, '--storagectl', 'SATA Controller', '--port', 2, '--device', 0, '--type', 'hdd', '--medium', lvm_experiments_disk1_path]
      end
    end
    ```

    Данная конфигурация создаст новую виртуальную машину с двумя дополнительными неразмеченными дисками по 2.5 Гб.
    
    ## Ответ
    готово
    ```bash
    vagrant@vagrant:~$ lsblk
    NAME                      MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
    loop0                       7:0    0 55.4M  1 loop /snap/core18/2128
    loop1                       7:1    0 70.3M  1 loop /snap/lxd/21029
    loop2                       7:2    0 32.3M  1 loop /snap/snapd/12704
    sda                         8:0    0   64G  0 disk
    ├─sda1                      8:1    0    1M  0 part
    ├─sda2                      8:2    0    1G  0 part /boot
    └─sda3                      8:3    0   63G  0 part
      └─ubuntu--vg-ubuntu--lv 253:0    0 31.5G  0 lvm  /
    sdb                         8:16   0  2.5G  0 disk
    sdc                         8:32   0  2.5G  0 disk
    ```
    
    ---
    
1. Используя `fdisk`, разбейте первый диск на 2 раздела: 2 Гб, оставшееся пространство.
    ## Ответ
    Готово
    ```bash
    vagrant@vagrant:~$ lsblk
    NAME                      MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
    loop0                       7:0    0 55.4M  1 loop /snap/core18/2128
    loop1                       7:1    0 70.3M  1 loop /snap/lxd/21029
    loop3                       7:3    0 55.5M  1 loop /snap/core18/2284
    loop4                       7:4    0 43.6M  1 loop /snap/snapd/14978
    loop5                       7:5    0 61.9M  1 loop /snap/core20/1376
    loop6                       7:6    0 67.9M  1 loop /snap/lxd/22526
    sda                         8:0    0   64G  0 disk
    ├─sda1                      8:1    0    1M  0 part
    ├─sda2                      8:2    0    1G  0 part /boot
    └─sda3                      8:3    0   63G  0 part
      └─ubuntu--vg-ubuntu--lv 253:0    0 31.5G  0 lvm  /
    sdb                         8:16   0  2.5G  0 disk
    ├─sdb1                      8:17   0    2G  0 part
    └─sdb2                      8:18   0  511M  0 part
    sdc                         8:32   0  2.5G  0 disk
    ```
    
    ---
    
1. Используя `sfdisk`, перенесите данную таблицу разделов на второй диск.
    ## Ответ
    готово
    ```bash
    vagrant@vagrant:~$ sudo sfdisk -d /dev/sdb| sudo sfdisk --force /dev/sdc
    ```
    ```bash
    vagrant@vagrant:~$ lsblk
    NAME                      MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
    loop0                       7:0    0 55.4M  1 loop /snap/core18/2128
    loop1                       7:1    0 70.3M  1 loop /snap/lxd/21029
    loop3                       7:3    0 55.5M  1 loop /snap/core18/2284
    loop4                       7:4    0 43.6M  1 loop /snap/snapd/14978
    loop5                       7:5    0 61.9M  1 loop /snap/core20/1376
    loop6                       7:6    0 67.9M  1 loop /snap/lxd/22526
    sda                         8:0    0   64G  0 disk
    ├─sda1                      8:1    0    1M  0 part
    ├─sda2                      8:2    0    1G  0 part /boot
    └─sda3                      8:3    0   63G  0 part
      └─ubuntu--vg-ubuntu--lv 253:0    0 31.5G  0 lvm  /
    sdb                         8:16   0  2.5G  0 disk
    ├─sdb1                      8:17   0    2G  0 part
    └─sdb2                      8:18   0  511M  0 part
    sdc                         8:32   0  2.5G  0 disk
    ├─sdc1                      8:33   0    2G  0 part
    └─sdc2                      8:34   0  511M  0 part
    ```
        
    ---
    
1. Соберите `mdadm` RAID1 на паре разделов 2 Гб.
    ## Ответ
    ```bash
    vagrant@vagrant:~$ sudo mdadm --create --verbose /dev/md1 -l 1 -n 2 /dev/sd{b1,c1}
    ```
    ```bash
    vagrant@vagrant:~$ lsblk
    NAME                      MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT
    loop0                       7:0    0 55.4M  1 loop  /snap/core18/2128
    loop1                       7:1    0 70.3M  1 loop  /snap/lxd/21029
    loop3                       7:3    0 55.5M  1 loop  /snap/core18/2284
    loop4                       7:4    0 43.6M  1 loop  /snap/snapd/14978
    loop5                       7:5    0 61.9M  1 loop  /snap/core20/1376
    loop6                       7:6    0 67.9M  1 loop  /snap/lxd/22526
    sda                         8:0    0   64G  0 disk
    ├─sda1                      8:1    0    1M  0 part
    ├─sda2                      8:2    0    1G  0 part  /boot
    └─sda3                      8:3    0   63G  0 part
      └─ubuntu--vg-ubuntu--lv 253:0    0 31.5G  0 lvm   /
    sdb                         8:16   0  2.5G  0 disk
    ├─sdb1                      8:17   0    2G  0 part
    │ └─md1                     9:1    0    2G  0 raid1
    └─sdb2                      8:18   0  511M  0 part
    sdc                         8:32   0  2.5G  0 disk
    ├─sdc1                      8:33   0    2G  0 part
    │ └─md1                     9:1    0    2G  0 raid1
    └─sdc2                      8:34   0  511M  0 part
    ```
       
    ---
    
1. Соберите `mdadm` RAID0 на второй паре маленьких разделов.
    ## Ответ
    ```bash
    vagrant@vagrant:~$ sudo mdadm --create --verbose /dev/md0 -l 0 -n 2 /dev/sd{b2,c2}
    ```
    ```bash
    vagrant@vagrant:~$ lsblk
    NAME                      MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT
    loop0                       7:0    0 55.4M  1 loop  /snap/core18/2128
    loop1                       7:1    0 70.3M  1 loop  /snap/lxd/21029
    loop3                       7:3    0 55.5M  1 loop  /snap/core18/2284
    loop4                       7:4    0 43.6M  1 loop  /snap/snapd/14978
    loop5                       7:5    0 61.9M  1 loop  /snap/core20/1376
    loop6                       7:6    0 67.9M  1 loop  /snap/lxd/22526
    sda                         8:0    0   64G  0 disk
    ├─sda1                      8:1    0    1M  0 part
    ├─sda2                      8:2    0    1G  0 part  /boot
    └─sda3                      8:3    0   63G  0 part
      └─ubuntu--vg-ubuntu--lv 253:0    0 31.5G  0 lvm   /
    sdb                         8:16   0  2.5G  0 disk
    ├─sdb1                      8:17   0    2G  0 part
    │ └─md1                     9:1    0    2G  0 raid1
    └─sdb2                      8:18   0  511M  0 part
      └─md0                     9:0    0 1018M  0 raid0
    sdc                         8:32   0  2.5G  0 disk
    ├─sdc1                      8:33   0    2G  0 part
    │ └─md1                     9:1    0    2G  0 raid1
    └─sdc2                      8:34   0  511M  0 part
      └─md0                     9:0    0 1018M  0 raid0
    ```
       
    ---
    
1. Создайте 2 независимых PV на получившихся md-устройствах.
    ## Ответ
    ```bash
    vagrant@vagrant:~$ sudo pvcreate /dev/md1 /dev/md0
    Physical volume "/dev/md1" successfully created.
    Physical volume "/dev/md0" successfully created.
    ```
       
    ---
    
1. Создайте общую volume-group на этих двух PV.
    ## Ответ
    ```bash
    vagrant@vagrant:~$ sudo vgcreate vg1 /dev/md1 /dev/md0
    Volume group "vg1" successfully created
    ```
    ```bash
    vagrant@vagrant:~$ sudo vgs
      VG        #PV #LV #SN Attr   VSize   VFree
      ubuntu-vg   1   1   0 wz--n- <63.00g <31.50g
      vg1         2   0   0 wz--n-  <2.99g  <2.99g
    ```
       
    ---
    
1. Создайте LV размером 100 Мб, указав его расположение на PV с RAID0.
    ## Ответ
    ```bash
    vagrant@vagrant:~$ sudo lvcreate -L 100M vg1 /dev/md0
    Logical volume "lvol0" created.
    vagrant@vagrant:~$ sudo lvs
      LV        VG        Attr       LSize   Pool Origin Data%  Meta%  Move Log Cpy%Sync Convert
      ubuntu-lv ubuntu-vg -wi-ao----  31.50g
      lvol0     vg1       -wi-a----- 100.00m
    ```
       
    ---
    
1. Создайте `mkfs.ext4` ФС на получившемся LV.
    ## Ответ
    ```bash
    vagrant@vagrant:~$ sudo mkfs.ext4 /dev/vg1/lvol0
    mke2fs 1.45.5 (07-Jan-2020)
    Creating filesystem with 25600 4k blocks and 25600 inodes

    Allocating group tables: done
    Writing inode tables: done
    Creating journal (1024 blocks): done
    Writing superblocks and filesystem accounting information: done
    ```
       
    ---
    
1. Смонтируйте этот раздел в любую директорию, например, `/tmp/new`.
    ## Ответ
    ```bash
    vagrant@vagrant:~$ mkdir /tmp/new
    vagrant@vagrant:~$ sudo mount /dev/vg1/lvol0 /tmp/new
    vagrant@vagrant:~$ lsblk
    NAME                      MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT
    loop0                       7:0    0 55.4M  1 loop  /snap/core18/2128
    loop1                       7:1    0 70.3M  1 loop  /snap/lxd/21029
    loop3                       7:3    0 55.5M  1 loop  /snap/core18/2284
    loop4                       7:4    0 43.6M  1 loop  /snap/snapd/14978
    loop5                       7:5    0 61.9M  1 loop  /snap/core20/1376
    loop6                       7:6    0 67.9M  1 loop  /snap/lxd/22526
    sda                         8:0    0   64G  0 disk
    ├─sda1                      8:1    0    1M  0 part
    ├─sda2                      8:2    0    1G  0 part  /boot
    └─sda3                      8:3    0   63G  0 part
      └─ubuntu--vg-ubuntu--lv 253:0    0 31.5G  0 lvm   /
    sdb                         8:16   0  2.5G  0 disk
    ├─sdb1                      8:17   0    2G  0 part
    │ └─md1                     9:1    0    2G  0 raid1
    └─sdb2                      8:18   0  511M  0 part
      └─md0                     9:0    0 1018M  0 raid0
        └─vg1-lvol0           253:1    0  100M  0 lvm   /tmp/new
    sdc                         8:32   0  2.5G  0 disk
    ├─sdc1                      8:33   0    2G  0 part
    │ └─md1                     9:1    0    2G  0 raid1
    └─sdc2                      8:34   0  511M  0 part
      └─md0                     9:0    0 1018M  0 raid0
        └─vg1-lvol0           253:1    0  100M  0 lvm   /tmp/new
    ```
       
    ---
    
1. Поместите туда тестовый файл, например `wget https://mirror.yandex.ru/ubuntu/ls-lR.gz -O /tmp/new/test.gz`.
    ## Ответ
    ```bash
    vagrant@vagrant:/tmp/new$ ls -l
    total 21720
    drwx------ 2 root root    16384 Mar 14 16:20 lost+found
    -rw-r--r-- 1 root root 22223710 Mar 14 15:31 test.gz
    ```
       
    ---
    
1. Прикрепите вывод `lsblk`.
    ## Ответ
    ```bash
    vagrant@vagrant:/tmp/new$ lsblk
    NAME                      MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT
    loop0                       7:0    0 55.4M  1 loop  /snap/core18/2128
    loop1                       7:1    0 70.3M  1 loop  /snap/lxd/21029
    loop3                       7:3    0 55.5M  1 loop  /snap/core18/2284
    loop4                       7:4    0 43.6M  1 loop  /snap/snapd/14978
    loop5                       7:5    0 61.9M  1 loop  /snap/core20/1376
    loop6                       7:6    0 67.9M  1 loop  /snap/lxd/22526
    sda                         8:0    0   64G  0 disk
    ├─sda1                      8:1    0    1M  0 part
    ├─sda2                      8:2    0    1G  0 part  /boot
    └─sda3                      8:3    0   63G  0 part
      └─ubuntu--vg-ubuntu--lv 253:0    0 31.5G  0 lvm   /
    sdb                         8:16   0  2.5G  0 disk
    ├─sdb1                      8:17   0    2G  0 part
    │ └─md1                     9:1    0    2G  0 raid1
    └─sdb2                      8:18   0  511M  0 part
      └─md0                     9:0    0 1018M  0 raid0
        └─vg1-lvol0           253:1    0  100M  0 lvm   /tmp/new
    sdc                         8:32   0  2.5G  0 disk
    ├─sdc1                      8:33   0    2G  0 part
    │ └─md1                     9:1    0    2G  0 raid1
    └─sdc2                      8:34   0  511M  0 part
      └─md0                     9:0    0 1018M  0 raid0
        └─vg1-lvol0           253:1    0  100M  0 lvm   /tmp/new
    ```
       
    ---
        
1. Протестируйте целостность файла:

    ```bash
    root@vagrant:~# gzip -t /tmp/new/test.gz
    root@vagrant:~# echo $?
    0
    ```
    ## Ответ
    ```bash
    vagrant@vagrant:/tmp/new$ sudo gzip -t /tmp/new/test.gz
    vagrant@vagrant:/tmp/new$ sudo echo $?
    0
    ``` 
       
    ---
    
1. Используя pvmove, переместите содержимое PV с RAID0 на RAID1.
    ## Ответ
    ```bash
    vagrant@vagrant:/tmp/new$ sudo pvmove /dev/md0
      /dev/md0: Moved: 16.00%
      /dev/md0: Moved: 100.00%
    vagrant@vagrant:/tmp/new$ lsblk
    NAME                      MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT
    loop0                       7:0    0 55.4M  1 loop  /snap/core18/2128
    loop1                       7:1    0 70.3M  1 loop  /snap/lxd/21029
    loop3                       7:3    0 55.5M  1 loop  /snap/core18/2284
    loop4                       7:4    0 43.6M  1 loop  /snap/snapd/14978
    loop5                       7:5    0 61.9M  1 loop  /snap/core20/1376
    loop6                       7:6    0 67.9M  1 loop  /snap/lxd/22526
    sda                         8:0    0   64G  0 disk
    ├─sda1                      8:1    0    1M  0 part
    ├─sda2                      8:2    0    1G  0 part  /boot
    └─sda3                      8:3    0   63G  0 part
      └─ubuntu--vg-ubuntu--lv 253:0    0 31.5G  0 lvm   /
    sdb                         8:16   0  2.5G  0 disk
    ├─sdb1                      8:17   0    2G  0 part
    │ └─md1                     9:1    0    2G  0 raid1
    │   └─vg1-lvol0           253:1    0  100M  0 lvm   /tmp/new
    └─sdb2                      8:18   0  511M  0 part
      └─md0                     9:0    0 1018M  0 raid0
    sdc                         8:32   0  2.5G  0 disk
    ├─sdc1                      8:33   0    2G  0 part
    │ └─md1                     9:1    0    2G  0 raid1
    │   └─vg1-lvol0           253:1    0  100M  0 lvm   /tmp/new
    └─sdc2                      8:34   0  511M  0 part
      └─md0                     9:0    0 1018M  0 raid0
    ```
       
    ---
    
1. Сделайте `--fail` на устройство в вашем RAID1 md.
    ## Ответ
    ```bash
    vagrant@vagrant:/tmp/new$ sudo mdadm /dev/md1 --fail /dev/sdb1
    mdadm: set /dev/sdb1 faulty in /dev/md1
    vagrant@vagrant:/tmp/new$ sudo mdadm --detail /dev/md1
    /dev/md1:
               Version : 1.2
         Creation Time : Mon Mar 14 15:58:06 2022
            Raid Level : raid1
            Array Size : 2094080 (2045.00 MiB 2144.34 MB)
         Used Dev Size : 2094080 (2045.00 MiB 2144.34 MB)
          Raid Devices : 2
         Total Devices : 2
           Persistence : Superblock is persistent

           Update Time : Mon Mar 14 16:32:21 2022
                 State : clean, degraded
        Active Devices : 1
       Working Devices : 1
        Failed Devices : 1
         Spare Devices : 0

    Consistency Policy : resync

                  Name : vagrant:1  (local to host vagrant)
                  UUID : 9fad996f:59299fe6:1d5c78f0:f362721f
                Events : 19

        Number   Major   Minor   RaidDevice State
           -       0        0        0      removed
           1       8       33        1      active sync   /dev/sdc1

           0       8       17        -      faulty   /dev/sdb1
    ```
       
    ---
    
1. Подтвердите выводом `dmesg`, что RAID1 работает в деградированном состоянии.
    ## Ответ
    ```bash
    vagrant@vagrant:/tmp/new$ dmesg |grep md1
    [ 2564.189681] md/raid1:md1: not clean -- starting background reconstruction
    [ 2564.189683] md/raid1:md1: active with 2 out of 2 mirrors
    [ 2564.189703] md1: detected capacity change from 0 to 2144337920
    [ 2564.190975] md: resync of RAID array md1
    [ 2574.840361] md: md1: resync done.
    [ 4617.796907] md/raid1:md1: Disk failure on sdb1, disabling device.
                   md/raid1:md1: Operation continuing on 1 devices.
    ```
       
    ---
    
1. Протестируйте целостность файла, несмотря на "сбойный" диск он должен продолжать быть доступен:

    ```bash
    root@vagrant:~# gzip -t /tmp/new/test.gz
    root@vagrant:~# echo $?
    0
    ```
    ## Ответ
    ```bash
    vagrant@vagrant:/tmp/new$ gzip -t /tmp/new/test.gz
    vagrant@vagrant:/tmp/new$ echo $?
    0
    ```
       
    ---
    
1. Погасите тестовый хост, `vagrant destroy`.
    ## Ответ
    готово
 ---

## Как сдавать задания

Обязательными к выполнению являются задачи без указания звездочки. Их выполнение необходимо для получения зачета и диплома о профессиональной переподготовке.

Задачи со звездочкой (*) являются дополнительными задачами и/или задачами повышенной сложности. Они не являются обязательными к выполнению, но помогут вам глубже понять тему.

Домашнее задание выполните в файле readme.md в github репозитории. В личном кабинете отправьте на проверку ссылку на .md-файл в вашем репозитории.

Также вы можете выполнить задание в [Google Docs](https://docs.google.com/document/u/0/?tgif=d) и отправить в личном кабинете на проверку ссылку на ваш документ.
Название файла Google Docs должно содержать номер лекции и фамилию студента. Пример названия: "1.1. Введение в DevOps — Сусанна Алиева".

Если необходимо прикрепить дополнительные ссылки, просто добавьте их в свой Google Docs.

Перед тем как выслать ссылку, убедитесь, что ее содержимое не является приватным (открыто на комментирование всем, у кого есть ссылка), иначе преподаватель не сможет проверить работу. Чтобы это проверить, откройте ссылку в браузере в режиме инкогнито.

[Как предоставить доступ к файлам и папкам на Google Диске](https://support.google.com/docs/answer/2494822?hl=ru&co=GENIE.Platform%3DDesktop)

[Как запустить chrome в режиме инкогнито ](https://support.google.com/chrome/answer/95464?co=GENIE.Platform%3DDesktop&hl=ru)

[Как запустить  Safari в режиме инкогнито ](https://support.apple.com/ru-ru/guide/safari/ibrw1069/mac)

Любые вопросы по решению задач задавайте в чате Slack.

---
