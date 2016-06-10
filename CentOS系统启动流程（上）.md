## CentOS 系统启动流程（上） ##

作为系统运维人员，详细的了解操作系统的启动流程，对于我们日常排除故障大有益处，遇到相关的问题处理，能快速定位，迅速锁定关键点。

下面详细介绍一下， CentOS 系统的启动过程，以供各位参考。由于 linux 各个发行版使用的启动方法略有不同，比如 CentOS5 使用的是 initd ， CentOS6 使用的是较为接近的 Upstart ，而 CentOS7 则是使用画风完全不同的 Systemd ，因而，对于其中有区别的部分，我也会对应不同的发行版本来分别介绍。

一个基本的操作系统，无非就是由内核 + 系统级别的库 + 应用程序所组成。其中，内核负责进行内存管理、进程管理、安全管理、网络管理以及硬件驱动程序的管理。库提供了上层应用程序向下层操作系统的调用接口。应用程序，顾名思义，就是能提供各种功能各种服务的软件了。这其中，内核是整个系统的根本，没有内核，则应用程序也无法单独存在。因而，每个操作系统，内核是必不可少的，想要使用电脑，则必需先启动内核。因而，操作系统的启动，实际上也就是内核启动的过程。

回到正题，一般操作系统启动的过程，大致可分为以下**几个步骤**：

**加电自检 (POST)–>BootLoader 选择引导的内核 –> 内核启动，建立内核空间 –> 加载根文件系统 –> 建立用户空间，并启动用户空间的第一个程序，然后创建交互式接口，等待用户的操作指令**

**加电自检 (POST)** ：

通过固化在主板上 CMOS 的 ROM 芯片，执行指定程序，进行硬件检测。该步骤主要检查硬件几大部件， CPU 、主板、内存、显卡等设备，维持计算机运行的主要部件。如设备有问题，自检不通过，设备也点不亮。当然，也会顺带检测其它一些非必要的硬件设备，比如外设：鼠标键盘网卡声卡等。

**BootLoader **：

BIOS(Basic Input and Output System) 设置里，有个选项是关于引导顺序 (BOOT Sequence) 的，加电自检完成后，系统会根据 BOOT Sequence 里设定的顺序，查找可用的 MBR( 主引导记录 ) ，一旦找到设备有 MBR( 就是第一个找到的 MBR 设备 ) ，则会选择从该设备引导系统。 MBR 记录中，有 bootloader 程序，大小为 446 字节，该部分记录了引导系统的重要信息。该程序的主要功能，是提供一个菜单，允许用户选择要启动的系统或不同的内核版本，把用户选定的内核装载到内存中的特定空间中，解压、展开，并把系统控制权移交给内核，从而完成内核的引导。

这里插入一段小插曲，以前比较老的系统， BootLoader 的任务由 LILO(LInux LOader) 的软件所承担 , 而该软件也能很好的完成它的任务。因为以前的硬盘容量都比较小，因而 446 字节的信息描述足以完成对内核的加载。而随着现今硬盘容量的激增，每个分区都很大，而内核程序有可以保存在每一个分区中，这样，对于大容量硬盘， LILO 则显得有点力不从心了。不过 Linux 界从来都不缺明星呀，新一代的 BootLoader 软件 –GRUB: GRand Unified Bootloader (GRUB) 闪亮登场。

GRUB 传统版本用于 CentOS5 、 6, 版本号是 0.X ，新的 CentOS7 则升级到 1.X 版本。 GRUB 采用了分阶段运行的方式，成功的绕开了 446 字节的限制，实现了对大容量硬盘的支持。第 1 阶段， GRUB 依然是驻留在 MBR 的 bootloader 中，这一阶段的 BRUB ，主要完成对内核所在设备的链接，找到内核驻留到的存储设备。然后， GRUB 有个过渡阶段，可称为 1.5 阶段吧，该阶段利用找到的存储设备上的文件，识别内核所在硬盘分区上的文件系统，加载内核所在设备的驱动程序。能识别内核所在硬盘分区的文件系统，事情就好办了，第 2 阶段，将内核加载到内存的特定位置，运行，并将系统的控制权移交到该内核。至此，内核完成加载并开始启动。

**内核启动，建立内核空间，加载根文件系统 – ，建立用户空间**：

Kernel 启动后，会进行以下操作：

	自身初始化 ;
	
	探测可识别到的所有硬件设备；
	
	加载硬件驱动程序：（有可能会借助于 ramdisk 加载驱动）；
	
	以只读方式挂载根文件系统；
	
	运行用户空间的第一个应用程序；

其中用户空间的第一个应用程序的创建，各个发行版本因应使用的技术，在实现上略有不同，在 CentOS5 上沿用的是 sysv 风格的 initd ；而 CentOS6 使用的是在 initd 升级改良而来的 Upstart ； CentOS7 ，则采用了全新的 systemd 技术。鉴于 CentOS5 与 CentOS6 采用的技术较为雷同，在此，以 CentOS5 所使用的 initd 进行讲解，至于 CentOS7 所使用的 systemd 技术，我会在下篇中说明，在这里先卖个小广告，敬请大家期待。

CentOS5 运行用户空间的第一个应用程序是 /sbin/init ， init 以守护进程的形式而存在，且是所有用户空间进程的父进程，所有用户空间进程均由 init 进程创建派生而来。同时，在 init 运行的同时， init 会利用脚本程序，对系统环境进行大量的操作，以便完成系统初始化。

对于系统初始化，我们特别定制了一个特殊的脚本： /etc/rc.d/rc.sysinit 。这个脚本在系统初始化时运行，并执行一些特殊的操作，其主要实现的功能有：

	(1) 设置主机名：
	
	(2) 设置欢迎信息：
	
	(3) 激活 udev 和 selinux
	
	(4) 挂载 /etc/fstab 文件中定义的文件系统
	
	(5) 检测根文件系统，并以读写方式重新挂载根文件系统
	
	(6) 设置系统时钟
	
	(7) 激活 swap 设备
	
	(8) 根据 /etc/sysctl.conf 文件设置内核参数
	
	(9) 激活 lvm 及 software raid 设备
	
	(10) 加载额外设备的驱动程序
	
	(11) 清理操作

然后， CentOS 有个运行级别的概念。什么是运行级别呢？运行级别就是为了系统的运行或维护等应用目的而设定的运行等级。

CentOS5/6 有 7 个运行级别，分别是：

	0 ：关机
	
	1 ：单用户模式 (root, 无须登录，无需密码 ),single, 维护模式
	
	2 ：多用户模式，会启动网络功能，但不会启动 NFS ：维护模式
	
	3 ：多用户模式，正常模式，文本界面
	
	4 ：预留级别，暂不使用，但可视为同 3 级别一样
	
	5 ：多用户模式，正常模式，图形界面
	
	6 ：重启系统
	
	其中，默认级别是级别 3 或级别 5

Init 程序运行时，会读取 /etc/inittab 的配置文件，根据配置文件的不同而执行相应的动作。这里贴出一个 inittab 配置文件的例子：

	[root@www ~]# cat /etc/inittab
	
	# inittab is only used by upstart for the default runlevel.
	
	#
	
	# ADDING OTHER CONFIGURATION HERE WILL HAVE NO EFFECT ON YOUR SYSTEM.
	
	#
	
	# System initialization is started by /etc/init/rcS.conf
	
	#
	
	# Individual runlevels are started by /etc/init/rc.conf
	
	#
	
	# Ctrl-Alt-Delete is handled by /etc/init/control-alt-delete.conf
	
	#
	
	# Terminal gettys are handled by /etc/init/tty.conf and /etc/init/serial.conf,
	
	# with configuration in /etc/sysconfig/init.
	
	#
	
	# For information on how to write upstart event handlers, or how
	
	# upstart works, see init(5), init(8), and initctl(8).
	
	#
	
	# Default runlevel. The runlevels used are:
	
	#   0 – halt (Do NOT set initdefault to this)
	
	#   1 – Single user mode
	
	#   2 – Multiuser, without NFS (The same as 3, if you do not have networking)
	
	#   3 – Full multiuser mode
	
	#   4 – unused
	
	#   5 – X11
	
	#   6 – reboot (Do NOT set initdefault to this)
	
	#

id:3:initdefault:

文件前面的都是注释说明，实际只有一行，即最后一行是实际配置。它的格式为：

id:runlevel:action:process

其中：

Id ：就是每行的 id 值，不重复即可；

Runlevel ：就是上面提到的运行级别的数值；

Action:action 分别有如下的动作：

wait: 切换至此级别运行一次

respawn: 此 process 终止，就重新启动之

initdefault: 设定默认运行级别 ,  process 省略

sysinit: 设定系统初始化方式，此处一般为指定 /etc/rc.d/rc.sysint;

上面例子中的： id:3:initdefault:  # 就是默认运行 3 级别的意思

划分了运行级别，到底有什么作用呢？让我们看看 /etc/rc.d 目录下的内容：

	[root@www /]# ls -lh /etc/rc.d
	
	total 60K
	
	drwxr-xr-x. 2 root root 4.0K Apr  7 18:52 init.d
	
	-rwxr-xr-x. 1 root root 2.6K Oct 16  2014 rc
	
	drwxr-xr-x. 2 root root 4.0K Apr  7 18:53 rc0.d
	
	drwxr-xr-x. 2 root root 4.0K Apr  7 18:53 rc1.d
	
	drwxr-xr-x. 2 root root 4.0K Apr  7 18:53 rc2.d
	
	drwxr-xr-x. 2 root root 4.0K Apr  7 18:53 rc3.d
	
	drwxr-xr-x. 2 root root 4.0K Apr  7 18:53 rc4.d
	
	drwxr-xr-x. 2 root root 4.0K Apr  7 18:53 rc5.d
	
	drwxr-xr-x. 2 root root 4.0K Apr  7 18:53 rc6.d
	
	-rwxr-xr-x. 1 root root  340 Dec 29 23:22 rc.local
	
	-rwxr-xr-x. 1 root root  20K Oct 16  2014 rc.sysinit

这里， rc0.d 到 rc6.d 几个目录，对应的正是我们之前设置的 7 个运行级别。聪明的小伙伴看到这里一定猜到了什么了。我们再选 rc3.d 看看：

	[root@www /]# ls -lh /etc/rc.d/rc3.d/
	
	total 0
	
	lrwxrwxrwx. 1 root root 16 Dec 25 06:15 K01smartd -> ../init.d/smartd
	
	lrwxrwxrwx. 1 root root 17 Dec 25 06:10 K02oddjobd -> ../init.d/oddjobd
	
	.
	
	.
	
	.
	
	lrwxrwxrwx. 1 root root 18 Dec 29 22:33 K92iptables -> ../init.d/iptables
	
	lrwxrwxrwx. 1 root root 19 Dec 25 06:31 K95firstboot -> ../init.d/firstboot
	
	lrwxrwxrwx. 1 root root 14 Dec 25 06:15 K99rngd -> ../init.d/rngd
	
	lrwxrwxrwx. 1 root root 17 Dec 25 06:13 S01sysstat -> ../init.d/sysstat
	
	lrwxrwxrwx. 1 root root 22 Dec 25 06:14 S02lvm2-monitor -> ../init.d/lvm2-monitor
	
	lrwxrwxrwx. 1 root root 22 Dec 25 06:36 S03vmware-tools -> ../init.d/vmware-tools
	
	lrwxrwxrwx. 1 root root 17 Dec 25 06:07 S10network -> ../init.d/network
	
	.
	
	.
	
	.
	
	lrwxrwxrwx. 1 root root 15 Apr  7 18:53 S85httpd -> ../init.d/httpd
	
	lrwxrwxrwx. 1 root root 15 Dec 25 06:10 S90crond -> ../init.d/crond
	
	lrwxrwxrwx. 1 root root 13 Dec 25 06:00 S95atd -> ../init.d/atd
	
	lrwxrwxrwx. 1 root root 20 Dec 25 06:10 S99certmonger -> ../init.d/certmonger
	
	lrwxrwxrwx. 1 root root 11 Dec 25 06:07 S99local -> ../rc.local

鉴于编幅，中间省略了一大段，免得被人说我刷稿费呀。

虽然省略了不少内容，但各位有没有从中发现什么规律呢？

对，里面都是由 K01 某服务脚本 …K99 某服务脚本， S01 某服务脚本 …S99 某服务脚本组成。什么意思呢？ K## 开始的，对应的是关闭某某服务软件的脚本，而 S## 对应的，则是开启某某服务软件的脚本。比如： K92iptables 的功能，就是关闭 iptables 服务，而 S85httpd ，则是开启 httpd 服务了。

我们再来看看 httpd 服务

	lrwxrwxrwx. 1 root root 15 Apr  7 18:53 S85httpd -> ../init.d/httpd

S85httpd 链接到了上级目录 ../init.d/httpd ，因而，实际执行代码的脚本是在 /etc/rc.d/init.d 中的 httpd 脚本。这就是系统存放服务脚本的地方。

每个服务，我们都会按优先级编定不同的次序 (S##,K##) ，然后，在选择了相应的运行等级里，按次序运行该级别 K## 的脚本，以实现关闭该级别下的服务，然后，按次序运行该级别 S## 的脚本，以实现启动该级别下的服务。

系统脚务脚本与一般脚本的功能一样，只是在脚本开始的注释上有所要求，系统服务脚本的格式为：

	#!/bin/bash
	
	#
	
	#chkconfig: LLL nn nn

其中， LLL 是服务默认启动的级别，比如 LLL 为 3 ， 4 ， 5 ，则表示此服务默认在 3 级别、 4 级别、 5 级别下都是运行的。第一个 nn 则是用于启动的序号，比如上面的 httpd 服务， nn 是 85 ，则脚本名称就影射为 S85httpd ；第二个 nn 是关闭的序号，又比如上面的 iptabled 服务， nn 为 92 ，则脚本名称影射为 K92iptables 。

通过以上的规划，我们为系统的各种服务设置了各种场景。比如在多用户模式 3 级别下，我们可定制系统某些服务在内核启动后则自动加载运行，某些服务则不加载。在关机模式 0 级别下，我们可定制系统关闭某服务，然后才安全关机。

最后，系统在执行完上述的脚本命令后，还会默认启动 6 个虚拟终端，以等待用户登录，提供界面以执行交互式操作。

	tty1:2345:respawn:/usr/sbin/mingetty tty1
	
	tty2:2345:respawn:/usr/sbin/mingetty tty2
	
	Tty3:2345:respawn:/usr/sbin/mingetty tty3
	
	tty4:2345:respawn:/usr/sbin/mingetty tty4
	
	Tty5:2345:respawn:/usr/sbin/mingetty tty5
	
	tty6:2345:respawn:/usr/sbin/mingetty tty6

以上，就是 CentOS5 的系统启动全过程，是不是觉得眼花瞭乱呢，没关系，让我们总结一下整个过程：

CentOS5 的系统启动全过程：

加电自检 (POST)–>Boot Sequence(BIOS) –>BootLoader(MBR) 选择引导的内核 –> 内核启动，建立内核空间 –> 加载根文件系统 –> 建立用户空间，并启动用户空间的第一个程序 /sbin/init –> (/etc/inittab) –> 设置默认运行级别 –> 运行系统初始脚本、完成系统初始化 –> 关闭对应级别下需要关闭的服务，启动需要启动的服务 –> 设置登录终端 , 等待用户登录

这样一整理，是不是觉得整个启动过程清晰明瞭了  

至于 CentOS6 ，其启动过程与 5 其实是大同小异的，只是 CentOS6 的 init 配置文件为 /etc/init/*.conf 下的一堆配置文件，而 /etc/inittab 也为兼容 5 而依然存在。具体到二者的不同，表现在 CentOS5 的 init 执行脚本为顺序执行，因而在系统启动时会串行地执行一大堆的脚本命令，效率显得不高。而 CentOS6 在其之上稍作改变， init 的脚本执行机制类似于并行，因而 Upstart 的方式比 init 的方式来得高效。

**CentOS6 的系统启动全过程**：

加电自检 (POST)–>Boot Sequence(BIOS) –>BootLoader(MBR) 选择引导的内核 –> 内核启动，建立内核空间 –> 加载根文件系统 –> 建立用户空间，并启动用户空间的第一个程序 /sbin/init –> (/etc/inittab,/etc/init/*.conf) –> 设置默认运行级别 –> 运行系统初始脚本、完成系统初始化 –> 关闭对应级别下需要关闭的服务，启动需要启动的服务 –> 设置登录终端 , 等待用户登录

上述为 CentOS5 、 CentOS6 的系统启动过程，由于 CentOS7 采用的是 systemd 的机制，与上述的两种机制相比，发生了很大的变化，因而，我会在下篇中详述。

以上是我对 CentOS 系统启动过程的理解！作为初学者，我对 linux 的认识还是很肤浅，上述可能有不正确的地方，如有错漏，希望各位能及时指正，共同进步。

我的 QQ ： 153975050 

在此感谢马哥及马哥团队，在 linux 的道路上引领我一直向前！

小斌斌

2016-06-06