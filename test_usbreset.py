import unittest

from usbreset import USBReset

class TestDmesgParser(unittest.TestCase):

    def test_parse_match(self):
        line = '[ 8964.807279] xhci_hcd 0000:04:00.3: WARNING: Host System Error\n'

        result = USBReset.parse(line)
        expected = dict(time= 8964, device='xhci_hcd', id='0000:04:00.3', msg=': WARNING: Host System Error')

        self.assertEqual(result['time'], expected['time'])
        self.assertEqual(result['device'], expected['device'])
        self.assertEqual(result['id'], expected['id'])
        self.assertEqual(result['msg'], expected['msg'])
    
    def test_is_error(self):
        line = '[ 8964.807279] xhci_hcd 0000:04:00.3: WARNING: Host System Error'
        self.assertTrue(USBReset.is_error(line))

    def test_parse_nomatch(self):
        line = 'NOMATCH'
        self.assertRaises(Exception, USBReset.parse, line)

    def test_dmesg_log(self):
        matches = 0
        mismatches = 0
        expected_lines = 0
        for line in TestDmesgParser.DMESG_LOG.splitlines():
            expected_lines += 1
            try:
                USBReset.parse(line)
                matches += 1
            except Exception as ex:
                mismatches +=1
                continue
        
        self.assertTrue(matches > 0, f"Failed to match positives")
        self.assertEqual(matches+mismatches, expected_lines, f"Matches: {matches}, Mismatches: {mismatches}")

    DMESG_LOG = """
[    0.000000] x86/fpu: Supporting XSAVE feature 0x001: 'x87 floating point registers'
[    0.000000] x86/fpu: Supporting XSAVE feature 0x002: 'SSE registers'
[    0.000000] x86/fpu: Supporting XSAVE feature 0x004: 'AVX registers'
[    0.000000] x86/fpu: xstate_offset[2]:  576, xstate_sizes[2]:  256
[    0.000000] x86/fpu: Enabled xstate features 0x7, context size is 832 bytes, using 'compacted' format.
[    0.000000] signal: max sigframe size: 1776
[    0.000000] NX (Execute Disable) protection: active
[    0.000000] e820: update [mem 0xb2bcf018-0xb2bdc857] usable ==> usable
[    0.000000] e820: update [mem 0xb2bcf018-0xb2bdc857] usable ==> usable
[    0.000000] e820: update [mem 0xb2bc1018-0xb2bce457] usable ==> usable
[    0.000000] e820: update [mem 0xb2bc1018-0xb2bce457] usable ==> usable
[    0.000000] extended physical RAM map:
[    0.000000] reserve setup_data: [mem 0x0000000000000000-0x0000000000087fff] usable
[    0.000000] reserve setup_data: [mem 0x0000000000088000-0x00000000000bffff] reserved
[    0.000000] reserve setup_data: [mem 0x0000000000100000-0x0000000009bfffff] usable
[    0.000000] reserve setup_data: [mem 0x0000000009c00000-0x000000000a10ffff] reserved
[    0.000000] reserve setup_data: [mem 0x000000000a110000-0x000000000a1fffff] usable
[    0.000000] reserve setup_data: [mem 0x000000000a200000-0x000000000a209fff] ACPI NVS
[    0.000000] reserve setup_data: [mem 0x000000000a20a000-0x00000000b2bc1017] usable
[    0.000000] reserve setup_data: [mem 0x00000000b2bc1018-0x00000000b2bce457] usable
[    0.000000] reserve setup_data: [mem 0x00000000fee00000-0x00000000fee00fff] reserved
[    0.000000] reserve setup_data: [mem 0x00000000ff000000-0x00000000ffffffff] reserved
[    0.000000] reserve setup_data: [mem 0x0000000100000000-0x000000022f33ffff] usable
[    0.013853] ACPI: FACS 0x00000000BF357000 000040
[    0.013856] ACPI: SSDT 0x00000000BF7F8000 00533D (v02 HPQOEM 84AE     00000002 ACPI 00040000)
[    0.013859] ACPI: UEFI 0x00000000BF7F7000 000236 (v01 HPQOEM 84AE     00000001 HP   00040000)
[    0.013862] ACPI: ASF! 0x00000000BF7F5000 0000A5 (v32 HPQOEM 84AE     00000001 HP   00040000)
[    0.013865] ACPI: BOOT 0x00000000BF7F4000 000028 (v01 HPQOEM 84AE     00000001 HP   00040000)
[    0.013891] ACPI: IHIS 0x00000000BF7E1000 000038 (v01 HPQOEM 84AE     00000001 HP   00040000)
[    0.013893] ACPI: SSDT 0x00000000BF7E0000 00013D (v01 HPQOEM 84AE     00001000 ACPI 00040000)
[    0.013896] ACPI: SSDT 0x00000000BF7D9000 0069B3 (v01 HPQOEM 84AE     00001000 ACPI 00040000)
[    0.013922] ACPI: SSDT 0x00000000BF7CD000 001AE8 (v01 HPQOEM 84AE     00000001 ACPI 00040000)
[    0.013925] ACPI: FPDT 0x00000000BF7CC000 000044 (v01 HPQOEM SLIC-MPC 00000002 HP   00040000)
[    0.013928] ACPI: BGRT 0x00000000BF7CB000 000038 (v01 HPQOEM 84AE     00000001 HP   00040000)
[    0.013930] ACPI: SSDT 0x00000000BF7C9000 001CC9 (v01 HPQOEM 84AE     00000001 ACPI 00040000)
[    0.013933] ACPI: Reserving FACP table memory at [mem 0xbf7f3000-0xbf7f310b]
[    0.013934] ACPI: Reserving DSDT table memory at [mem 0xbf7e6000-0xbf7ee37d]
[    0.013935] ACPI: Reserving FACS table memory at [mem 0xbf357000-0xbf35703f]
[    0.013936] ACPI: Reserving SSDT table memory at [mem 0xbf7f8000-0xbf7fd33c]
[    0.013937] ACPI: Reserving UEFI table memory at [mem 0xbf7f7000-0xbf7f7235]
[    0.013938] ACPI: Reserving ASF! table memory at [mem 0xbf7f5000-0xbf7f50a4]
[    0.014410]   Normal   [mem 0x0000000100000000-0x000000022f33ffff]
[    0.014411]   Device   empty
[    0.014412] Movable zone start for each node
[    0.014416]   node   0: [mem 0x0000000000001000-0x0000000000087fff]
[    0.014417]   node   0: [mem 0x0000000000100000-0x0000000009bfffff]
[    0.014423] Initmem setup node 0 [mem 0x0000000000001000-0x000000022f33ffff]
[    0.022431] On node 0, zone Normal: 2048 pages in unavailable ranges
[    0.022482] On node 0, zone Normal: 3264 pages in unavailable ranges
[    0.022931] ACPI: PM-Timer IO Port: 0x408
[    0.022939] ACPI: LAPIC_NMI (acpi_id[0x00] high edge lint[0x1])
[    0.022952] ACPI: LAPIC_NMI (acpi_id[0x0f] high edge lint[0x1])
[    0.022991] ACPI: INT_SRC_OVR (bus 0 bus_irq 0 global_irq 2 dfl dfl)
[    0.023024] smpboot: Allowing 16 CPUs, 12 hotplug CPUs
[    0.023049] PM: hibernation: Registered nosave memory: [mem 0x00000000-0x00000fff]
[    0.023084] clocksource: refined-jiffies: mask: 0xffffffff max_cycles: 0xffffffff, max_idle_ns: 7645519600211568 ns
[    0.028299] printk: log_buf_len individual max cpu contribution: 32768 bytes
[    0.029151] printk: log_buf_len: 1048576 bytes
[    0.029152] printk: early log buf free: 244896(93%)
[    0.030192] Dentry cache hash table entries: 1048576 (order: 11, 8388608 bytes, linear)
[    0.065960] ftrace: allocated 173 pages with 5 groups
[    0.066657] Dynamic Preempt: voluntary
[    0.066699] rcu: Preemptible hierarchical RCU implementation.
[    0.066702] 	Trampoline variant of Tasks RCU enabled.
[    0.066702] 	Rude variant of Tasks RCU enabled.
[    0.066703] 	Tracing variant of Tasks RCU enabled.
[    0.066703] rcu: RCU calculated value of scheduler-enlistment delay is 25 jiffies.
[    0.066704] rcu: Adjusting geometry for rcu_fanout_leaf=16, nr_cpu_ids=16
[    0.070570] NR_IRQS: 524544, nr_irqs: 1096, preallocated irqs: 16
[    0.070771] rcu: srcu_init: Setting srcu_struct sizes based on contention.
[    0.071074] Console: colour dummy device 80x25
[    0.071092] printk: console [tty0] enabled
[    0.072365] AMD-Vi: [Firmware Bug]: : IOAPIC[4] not in IVRS table
[    0.072373] AMD-Vi: [Firmware Bug]: : IOAPIC[5] not in IVRS table
[    0.072375] AMD-Vi: [Firmware Bug]: : No southbridge IOAPIC found
[    0.072378] AMD-Vi: Disabling interrupt remapping
[    0.072383] Switched APIC routing to physical flat.
[    0.073732] ..TIMER: vector=0x30 apic1=0 pin1=2 apic2=-1 pin2=-1
[    0.091350] clocksource: tsc-early: mask: 0xffffffffffffffff max_cycles: 0x23f792a4796, max_idle_ns: 440795312285 ns
[    0.091361] Calibrating delay loop (skipped), value calculated using timer frequency.. 4990.43 BogoMIPS (lpj=9980864)
[    0.091365] pid_max: default: 32768 minimum: 301
[    0.095392] LSM: Security Framework initializing
[    0.095422] AppArmor: AppArmor initialized
[    0.218571] ... bit width:              48
[    0.218571] ... generic registers:      6
[    0.218572] ... value mask:             0000ffffffffffff
[    0.218573] ... max period:             00007fffffffffff
[    0.218574] ... fixed-purpose events:   0
[    0.218574] ... event mask:             000000000000003f
[    0.218666] rcu: Hierarchical SRCU implementation.
[    0.232640] clocksource: jiffies: mask: 0xffffffff max_cycles: 0xffffffff, max_idle_ns: 7645041785100000 ns
[    0.232640] futex hash table entries: 4096 (order: 6, 262144 bytes, linear)
[    0.232640] pinctrl core: initialized pinctrl subsystem
[    0.235459] cpuidle: using governor ladder
[    0.266646] ACPI: PM: (supports S0 S3 S4 S5)
[    0.266647] ACPI: Using IOAPIC for interrupt routing
[    0.267053] PCI: Using host bridge windows from ACPI; if necessary, use "pci=nocrs" and report a bug
[    0.267054] PCI: Using E820 reservations for host bridge windows
[    0.267485] ACPI: Enabled 3 GPEs in block 00 to 1F
[    0.269919] ACPI: PM: Power Resource [P0ST]
[    0.269951] ACPI: PM: Power Resource [P3ST]
[    0.337426] ACPI Error: Aborting method \_SB.WLBU._STA due to previous error (AE_NOT_FOUND) (20220331/psparse-529)
[    0.341315] ACPI: PCI Root Bridge [PCI0] (domain 0000 [bus 00-ff])
[    0.341323] acpi PNP0A08:00: _OSC: OS supports [ExtendedConfig ASPM ClockPM Segments MSI EDR HPX-Type3]
[    0.341980] pci_bus 0000:00: root bus resource [mem 0x000d0000-0x000effff window]
[    0.341981] pci_bus 0000:00: root bus resource [mem 0xd0000000-0xefffffff window]
[    0.341983] pci_bus 0000:00: root bus resource [mem 0xf8000000-0xfed3ffff window]
[    0.341985] pci_bus 0000:00: root bus resource [bus 00-ff]
[    0.342360] pci 0000:00:01.1: [1022:15d3] type 01 class 0x060400
[    0.342488] pci 0000:00:01.1: PME# supported from D0 D3hot D3cold
[    0.342628] pci 0000:00:01.2: [1022:15d3] type 01 class 0x060400
[    0.342754] pci 0000:00:01.2: PME# supported from D0 D3hot D3cold
[    0.342886] pci 0000:00:01.3: [1022:15d3] type 01 class 0x060400
[    0.343011] pci 0000:00:01.3: PME# supported from D0 D3hot D3cold
[    0.343170] pci 0000:00:08.0: [1022:1452] type 00 class 0x060000
[    0.343273] pci 0000:00:08.1: [1022:15db] type 01 class 0x060400
[    0.343327] pci 0000:00:08.1: enabling Extended Tags
[    0.343396] pci 0000:00:08.1: PME# supported from D0 D3hot D3cold
[    0.343526] pci 0000:00:08.2: [1022:15dc] type 01 class 0x060400
[    0.347967] pci 0000:05:00.0: [1022:7901] type 00 class 0x010601
[    0.348043] pci 0000:05:00.0: reg 0x24: [mem 0xe0200000-0xe02007ff]
[    0.348065] pci 0000:05:00.0: enabling Extended Tags
[    0.348149] pci 0000:05:00.0: PME# supported from D3hot D3cold
[    0.349181] pci 0000:00:08.2: PCI bridge to [bus 05]
[    0.349191] pci 0000:00:08.2:   bridge window [mem 0xe0200000-0xe02fffff]
[    0.411832] ACPI: PCI: Interrupt link LNKA configured for IRQ 0
[    0.411837] ACPI: PCI: Interrupt link LNKA disabled
[    0.412053] ACPI: PCI: Interrupt link LNKB configured for IRQ 0
[    0.416629] ACPI: EC: interrupt unblocked
[    0.416631] ACPI: EC: event unblocked
[    0.416643] ACPI: EC: EC_CMD/EC_SC=0x66, EC_DATA=0x62
[    0.416645] ACPI: EC: GPE=0x3
[    0.416647] ACPI: \_SB_.PCI0.LPC0.EC0_: Boot DSDT EC initialization complete
[    0.416650] ACPI: \_SB_.PCI0.LPC0.EC0_: EC: Used to handle transactions and events
[    0.416709] iommu: Default domain type: Passthrough 
[    0.416709] SCSI subsystem initialized
[    0.416709] libata version 3.00 loaded.
[    0.416709] pps_core: LinuxPPS API ver. 1 registered
[    0.422748] e820: reserve RAM buffer [mem 0xbb57f000-0xbbffffff]
[    0.422749] e820: reserve RAM buffer [mem 0xbf800000-0xbfffffff]
[    0.422750] e820: reserve RAM buffer [mem 0x22f340000-0x22fffffff]
[    0.423381] pci 0000:04:00.0: vgaarb: setting as boot VGA device
[    0.423381] pci 0000:04:00.0: vgaarb: bridge control possible
[    0.423381] pci 0000:04:00.0: vgaarb: VGA device added: decodes=io+mem,owns=io+mem,locks=none
[    0.423381] vgaarb: loaded
[    0.424655] pnp: PnP ACPI init
[    0.425673] system 00:04: [io  0x04d0-0x04d1] has been reserved
[    0.425675] system 00:04: [io  0x04d6] has been reserved
[    0.425676] system 00:04: [io  0x0c00-0x0c01] has been reserved
[    0.425678] system 00:04: [io  0x0c14] has been reserved
[    0.425679] system 00:04: [io  0x0c50-0x0c52] has been reserved
[    0.500303] pci_bus 0000:04: resource 0 [io  0x1000-0x1fff]
[    0.500307] pci_bus 0000:05: resource 1 [mem 0xe0200000-0xe02fffff]
[    0.500467] pci 0000:04:00.1: D0 power state depends on 0000:04:00.0
[    0.500482] pci 0000:04:00.3: extending delay after power-on from D3hot to 20 msec
[    0.580356] PCI: CLS 64 bytes, default 64
[    0.792819] IPI shorthand broadcast: enabled
[    1.186074] sd 0:0:0:0: [sda] 500118192 512-byte logical blocks: (256 GB/238 GiB)
[    1.186089] sd 0:0:0:0: [sda] Write Protect is off
[    1.186096] sd 0:0:0:0: [sda] Mode Sense: 00 3a 00 00
[    1.186123] sd 0:0:0:0: [sda] Write cache: enabled, read cache: enabled, doesn't support DPO or FUA
[    1.186151] sd 0:0:0:0: [sda] Preferred minimum I/O size 512 bytes
[    1.202043]  sda: sda1 sda2
[    1.202203] sd 0:0:0:0: [sda] Attached SCSI disk
[    1.525652] psmouse serio1: synaptics: queried max coordinates: x [..5648], y [..4826]
[    1.715992] systemd[1]: Detected architecture x86-64.
[    1.715995] systemd[1]: Running in initial RAM disk.
[    1.716036] systemd[1]: No hostname configured, using default hostname.
[    1.716104] systemd[1]: Hostname set to <localhost>.
[    1.718348] systemd[1]: Failed to open libbpf, cgroup BPF features disabled: Operation not supported
[    1.766110] systemd[1]: /usr/lib/systemd/system/plymouth-start.service:15: Unit configured to use KillMode=none. This is unsafe, as it disables systemd's process lifecycle management for the service. Please update your service to use a safer KillMode=, such as 'mixed' or 'control-group'. Support for KillMode=none is deprecated and will eventually be removed.
[    1.778196] systemd[1]: Queued start job for default target Initrd Default Target.
[    1.778986] systemd[1]: Created slice Slice /system/systemd-cryptsetup.
[    1.779260] systemd[1]: Created slice Slice /system/systemd-hibernate-resume.
[    1.779324] systemd[1]: Reached target Initrd /usr File System.
[    1.779349] systemd[1]: Reached target Slice Units.
[    1.779369] systemd[1]: Reached target Swaps.
[    1.779382] systemd[1]: Reached target Timer Units.
[    1.779483] systemd[1]: Listening on Journal Socket (/dev/log).
[    1.779573] systemd[1]: Listening on Journal Socket.
[    1.779676] systemd[1]: Listening on udev Control Socket.
[    1.779749] systemd[1]: Listening on udev Kernel Socket.
[    1.779764] systemd[1]: Reached target Socket Units.
[    1.780816] systemd[1]: Started Entropy Daemon based on the HAVEGE algorithm.
[    1.781605] systemd[1]: Starting Create List of Static Device Nodes...
[    1.783231] systemd[1]: Starting Journal Service...
[    1.784289] systemd[1]: Starting Load Kernel Modules...
[    1.785123] systemd[1]: Starting Setup Virtual Console...
[    1.785813] systemd[1]: Finished Create List of Static Device Nodes.
[    1.786826] systemd[1]: Starting Create Static Device Nodes in /dev...
[    1.791010] bbswitch: loading out-of-tree module taints kernel.
[    1.791294] bbswitch: version 0.8
[    1.793169] systemd[1]: Finished Create Static Device Nodes in /dev.
[    1.813251] systemd[1]: Finished Setup Virtual Console.
[    1.813968] systemd[1]: Starting dracut ask for additional cmdline parameters...
[    1.829841] systemd[1]: Finished dracut ask for additional cmdline parameters.
[    1.830667] systemd[1]: Starting dracut cmdline hook...
[    1.833950] alua: device handler registered
[    1.834814] emc: device handler registered
[    1.835766] rdac: device handler registered
[    1.839376] systemd[1]: Started Journal Service.
[    1.845972] device-mapper: core: CONFIG_IMA_DISABLE_HTABLE is disabled. Duplicate IMA measurements will not be recorded in the IMA log.
[    1.846005] device-mapper: uevent: version 1.0.3
[    1.846059] device-mapper: ioctl: 4.47.0-ioctl (2022-07-28) initialised: dm-devel@redhat.com
[    1.849848] sd 0:0:0:0: Attached scsi generic sg0 type 0
[    2.073208] ACPI: video: Video Device [VGA1] (multi-head: yes  rom: no  post: no)
[    2.073847] acpi device:0b: registered as cooling_device4
[    2.073905] input: Video Bus as /devices/LNXSYSTM:00/LNXSYBUS:00/PNP0A08:00/device:0a/LNXVIDEO:01/input/input3
[    2.085727] wmi_bus wmi_bus-PNP0C14:00: WQBJ data block query control method not found
[    2.095350] sp5100_tco: SP5100/SB800 TCO WatchDog Timer Driver
[    2.095470] sp5100-tco sp5100-tco: Using 0xfeb00000 for watchdog MMIO address
[    2.103106] sp5100-tco sp5100-tco: initialized. heartbeat=60 sec (nowayout=0)
[    2.105253] ccp 0000:04:00.2: ccp enabled
[    2.111370] cryptd: max_cpu_qlen set to 1000
[    2.113061] ACPI: bus type USB registered
[    2.113097] usbcore: registered new interface driver usbfs
[    2.113107] usbcore: registered new interface driver hub
[    2.113706] usbcore: registered new device driver usb
[    2.120049] clocksource: Checking clocksource tsc synchronization from CPU 0 to CPUs 1-2.
[    2.120079] clocksource: Switched to clocksource hpet
[    2.215518] ACPI: battery: Slot [BAT1] (battery present)
[    2.222361] AVX2 version of gcm_enc/dec engaged.
[    2.222393] AES CTR mode by8 optimization enabled
[    2.241704] xhci_hcd 0000:04:00.3: xHCI Host Controller
[    2.241715] xhci_hcd 0000:04:00.3: new USB bus registered, assigned bus number 1
[    2.241907] xhci_hcd 0000:04:00.3: hcc params 0x0270ffe5 hci version 0x110 quirks 0x0000000840000410
[    2.242286] xhci_hcd 0000:04:00.3: xHCI Host Controller
[    2.242290] xhci_hcd 0000:04:00.3: new USB bus registered, assigned bus number 2
[    2.242294] xhci_hcd 0000:04:00.3: Host supports USB 3.1 Enhanced SuperSpeed
[    2.242365] usb usb1: New USB device found, idVendor=1d6b, idProduct=0002, bcdDevice= 5.19
[    2.242391] usb usb1: Product: xHCI Host Controller
[    2.245262] xhci_hcd 0000:04:00.4: xHCI Host Controller
[    2.245275] xhci_hcd 0000:04:00.4: new USB bus registered, assigned bus number 3
[    2.245449] xhci_hcd 0000:04:00.4: hcc params 0x0260ffe5 hci version 0x110 quirks 0x0000000840000410
[    2.245933] xhci_hcd 0000:04:00.4: xHCI Host Controller
[    2.245938] xhci_hcd 0000:04:00.4: new USB bus registered, assigned bus number 4
[    2.245941] xhci_hcd 0000:04:00.4: Host supports USB 3.1 Enhanced SuperSpeed
[    2.246017] usb usb3: New USB device found, idVendor=1d6b, idProduct=0002, bcdDevice= 5.19
[    2.246022] usb usb3: Product: xHCI Host Controller
[    2.246025] usb usb3: Manufacturer: Linux 5.19.10-1-default xhci-hcd
[    2.246160] hub 3-0:1.0: USB hub found
[    2.246171] hub 3-0:1.0: 2 ports detected
[    2.246534] hub 4-0:1.0: USB hub found
[    2.246542] hub 4-0:1.0: 1 port detected
[    3.919049] usb-storage 3-1:1.0: USB Mass Storage device detected
[    3.919279] scsi host1: usb-storage 3-1:1.0
[    3.919440] usbcore: registered new interface driver usb-storage
[    3.921587] usbcore: registered new interface driver uas
[    3.925476] [drm] amdgpu kernel modesetting enabled.
[    3.926464] amdgpu: Topology: Add APU node [0x0:0x0]
[    3.947510] Console: switching to colour dummy device 80x25
[    3.956056] usbcore: registered new interface driver usbhid
[    3.956062] usbhid: USB HID core driver
[    3.972172] amdgpu 0000:04:00.0: vgaarb: deactivate vga console
[    3.972440] [drm] register mmio size: 524288
[    3.972554] [drm] add ip block number 0 <soc15_common>
[    3.972557] [drm] add ip block number 1 <gmc_v9_0>
[    3.972560] [drm] add ip block number 2 <vega10_ih>
[    3.972561] [drm] add ip block number 3 <psp>
[    3.972563] [drm] add ip block number 4 <powerplay>
[    3.972566] [drm] add ip block number 5 <dm>
[    3.972568] [drm] add ip block number 6 <gfx_v9_0>
[    3.972571] [drm] add ip block number 7 <sdma_v4_0>
[    3.972573] [drm] add ip block number 8 <vcn_v1_0>
[    4.010073] [drm] VCN decode is enabled in VM mode
[    4.010074] [drm] VCN encode is enabled in VM mode
[    4.010075] [drm] JPEG decode is enabled in VM mode
[   18.254688] systemd[1]: Created slice Slice /system/getty.
[   18.255320] systemd[1]: Created slice Slice /system/modprobe.
[   18.255892] systemd[1]: Created slice Slice /system/systemd-fsck.
[   18.256242] systemd[1]: Created slice User and Session Slice.
[   18.256470] systemd[1]: Set up automount Arbitrary Executable File Formats File System Automount Point.
[   18.256598] systemd[1]: Reached target Block Device Preparation for /dev/mapper/cr_root.
[   18.256644] systemd[1]: Reached target Block Device Preparation for /dev/mapper/cr_swap.
[   18.256718] systemd[1]: Stopped target Switch Root.
[   18.256766] systemd[1]: Stopped target Initrd File Systems.
[   18.256799] systemd[1]: Stopped target Initrd Root File System.
[   18.256910] systemd[1]: Reached target Local Integrity Protected Volumes.
[   18.256997] systemd[1]: Reached target Remote File Systems.
[   18.257040] systemd[1]: Reached target Slice Units.
[   18.257112] systemd[1]: Reached target System Time Set.
[   18.257190] systemd[1]: Reached target Local Verity Protected Volumes.
[   18.257332] systemd[1]: Listening on Device-mapper event daemon FIFOs.
[   18.257805] systemd[1]: Listening on LVM2 poll daemon socket.
[   18.257931] systemd[1]: Listening on initctl Compatibility Named Pipe.
[   18.258342] systemd[1]: Listening on udev Control Socket.
[   18.258485] systemd[1]: Listening on udev Kernel Socket.
[   18.259707] systemd[1]: Activating swap /dev/disk/by-uuid/834b0484-52d9-4685-98bf-486eb9bee00d...
[   18.260859] systemd[1]: Mounting Huge Pages File System...
[   18.262285] systemd[1]: Mounting POSIX Message Queue File System...
[   18.264026] systemd[1]: Mounting Kernel Debug File System...
[   18.265513] systemd[1]: Mounting Kernel Trace File System...
[   18.267023] systemd[1]: Starting Load AppArmor profiles...
[   18.268801] systemd[1]: Starting Create List of Static Device Nodes...
[   18.270381] systemd[1]: Starting Monitoring of LVM2 mirrors, snapshots etc. using dmeventd or progress polling...
[   18.271987] systemd[1]: Starting Load Kernel Module configfs...
[   18.273398] systemd[1]: Starting Load Kernel Module drm...
[   18.274783] systemd[1]: Starting Load Kernel Module fuse...
[   18.274969] systemd[1]: plymouth-start.service: Deactivated successfully.
[   18.275011] systemd[1]: plymouth-start.service: Unit process 393 (plymouthd) remains running after unit stopped.
[   18.275214] systemd[1]: Stopped Show Plymouth Boot Screen.
[   18.275520] systemd[1]: Dispatch Password Requests to Console Directory Watch was skipped because of a failed condition check (ConditionPathExists=!/run/plymouth/pid).
[   18.275605] systemd[1]: plymouth-switch-root.service: Deactivated successfully.
[   18.275697] systemd[1]: Stopped Plymouth switch root service.
[   18.275938] systemd[1]: Stopped Journal Service.
[   18.276157] systemd[1]: Stopping Entropy Daemon based on the HAVEGE algorithm...
[   18.278931] systemd[1]: Starting Load Kernel Modules...
[   18.280410] Adding 16775164k swap on /dev/mapper/cr_swap.  Priority:-2 extents:1 across:16775164k FS
[   18.280987] systemd[1]: Starting Remount Root and Kernel File Systems...
[   18.282839] systemd[1]: Starting Coldplug All udev Devices...
[   18.288450] systemd[1]: Activated swap /dev/disk/by-uuid/834b0484-52d9-4685-98bf-486eb9bee00d.
[   18.289630] systemd[1]: haveged.service: Deactivated successfully.
[   18.290185] systemd[1]: Stopped Entropy Daemon based on the HAVEGE algorithm.
[   18.292028] systemd[1]: Mounted Huge Pages File System.
[   18.292578] systemd[1]: Mounted POSIX Message Queue File System.
[   18.292955] systemd[1]: Mounted Kernel Debug File System.
[   18.293591] systemd[1]: Mounted Kernel Trace File System.
[   18.294969] systemd[1]: Finished Create List of Static Device Nodes.
[   18.295910] systemd[1]: modprobe@drm.service: Deactivated successfully.
[   18.296578] systemd[1]: Finished Load Kernel Module drm.
[   18.296985] systemd[1]: Reached target Swaps.
[   18.300648] systemd[1]: Mounting Temporary Directory /tmp...
[   18.300878] bbswitch: version 0.8
[   18.300895] bbswitch: Found discrete VGA device 0000:04:00.0: \_SB_.PCI0.GP17.VGA_
[   18.300919] bbswitch: failed to evaluate \_SB_.PCI0.GP17.VGA_._DSM {0xF8,0xD8,0x86,0xA4,0xDA,0x0B,0x1B,0x47,0xA7,0x2B,0x60,0x42,0xA6,0xB5,0xBE,0xE0} 0x100 0x0 {0x00,0x00,0x00,0x00}: AE_NOT_FOUND
[   18.300930] bbswitch: failed to evaluate \_SB_.PCI0.GP17.VGA_._DSM {0xA0,0xA0,0x95,0x9D,0x60,0x00,0x48,0x4D,0xB3,0x4D,0x7E,0x5F,0xEA,0x12,0x9F,0xD4} 0x102 0x0 {0x00,0x00,0x00,0x00}: AE_NOT_FOUND
[   18.300933] bbswitch: No suitable _DSM call found.
[   18.303168] systemd[1]: Starting Journal Service...
[   18.303667] EXT4-fs (dm-0): re-mounted. Quota mode: none.
[   18.305075] systemd[1]: modprobe@configfs.service: Deactivated successfully.
[   18.305302] systemd[1]: Finished Load Kernel Module configfs.
[   18.305634] systemd[1]: Mounted Temporary Directory /tmp.
[   18.307418] systemd[1]: Mounting Kernel Configuration File System...
[   18.310049] systemd[1]: Finished Remount Root and Kernel File Systems.
[   18.311167] systemd[1]: Mounted Kernel Configuration File System.
[   18.311874] systemd[1]: First Boot Wizard was skipped because of a failed condition check (ConditionFirstBoot=yes).
[   18.313027] fuse: init (API version 7.36)
[   18.313199] systemd[1]: Rebuild Hardware Database was skipped because of a failed condition check (ConditionNeedsUpdate=/etc).
[   18.314900] systemd[1]: Starting Load/Save Random Seed...
[   18.315043] systemd[1]: Create System Users was skipped because of a failed condition check (ConditionNeedsUpdate=/etc).
[   18.317018] systemd[1]: Starting Create Static Device Nodes in /dev...
[   18.317692] systemd[1]: modprobe@fuse.service: Deactivated successfully.
[   18.317995] systemd[1]: Finished Load Kernel Module fuse.
[   18.319742] systemd[1]: Mounting FUSE Control File System...
[   18.322586] systemd[1]: Mounted FUSE Control File System.
[   18.337341] systemd[1]: Finished Load/Save Random Seed.
[   18.337750] systemd[1]: First Boot Complete was skipped because of a failed condition check (ConditionFirstBoot=yes).
[   18.339940] systemd[1]: Started Journal Service.
[   18.352485] systemd-journald[801]: Received client request to flush runtime journal.
[   18.750320] input: Power Button as /devices/LNXSYSTM:00/LNXPWRBN:00/input/input12
[   18.752607] ACPI: button: Power Button [PWRF]
[   18.779836] input: Wireless hotkeys as /devices/virtual/input/input13
[   18.809091] thermal LNXTHERM:00: registered as thermal_zone0
[   18.809096] ACPI: thermal: Thermal Zone [TSZ0] (60 C)
[   18.810139] thermal LNXTHERM:01: registered as thermal_zone1
[   18.810142] ACPI: thermal: Thermal Zone [TSZ2] (20 C)
[   18.819851] ACPI: AC: AC Adapter [ACAD] (on-line)
[   19.032087] cfg80211: Loading compiled-in X.509 certificates for regulatory database
[   19.032103] r8169 0000:02:00.0: can't disable ASPM; OS doesn't have ASPM control
[   19.420249] snd_hda_codec_realtek hdaudioC1D0: autoconfig for ALC236: line_outs=1 (0x14/0x0/0x0/0x0/0x0) type:speaker
[   19.420256] snd_hda_codec_realtek hdaudioC1D0:    speaker_outs=0 (0x0/0x0/0x0/0x0/0x0)
[   19.420259] snd_hda_codec_realtek hdaudioC1D0:    hp_outs=1 (0x21/0x0/0x0/0x0/0x0)
[   19.420262] snd_hda_codec_realtek hdaudioC1D0:    mono: mono_out=0x0
[   19.420263] snd_hda_codec_realtek hdaudioC1D0:    inputs:
[   19.420265] snd_hda_codec_realtek hdaudioC1D0:      Mic=0x19
[   19.420267] snd_hda_codec_realtek hdaudioC1D0:      Internal Mic=0x12
[   19.446238] rtw_8821ce 0000:03:00.0 wlo1: renamed from wlan0
[   19.519025] intel_rapl_common: Found RAPL domain package
[   19.519030] intel_rapl_common: Found RAPL domain core
[   20.898458] NET: Registered PF_BLUETOOTH protocol family
[   20.898459] Bluetooth: HCI device and connection manager initialized
[   20.898464] Bluetooth: HCI socket layer initialized
[   20.898466] Bluetooth: L2CAP socket layer initialized
[   20.898470] Bluetooth: SCO socket layer initialized
[   25.373734] bridge: filtering via arp/ip/ip6tables is no longer available by default. Update your scripts to load br_netfilter if you need this.
[   25.377944] Bridge firewalling registered
[   25.480865] NET: Registered PF_PACKET protocol family
[   25.625005] Initializing XFRM netlink socket
[   30.624235] wlo1: authenticate with 11:11:11:11:11:11
[   31.275706] wlo1: send auth to 11:11:11:11:11:11 (try 1/3)
[   31.611733] wlo1: authenticate with 11:11:11:11:11:11
[   31.611796] wlo1: send auth to 11:11:11:11:11:11 (try 1/3)
[   31.700111] wlo1: authenticated
[ 8272.767416] sd 0:0:0:0: [sda] Synchronizing SCSI cache
[ 8272.767529] sd 0:0:0:0: [sda] Stopping disk
[ 8273.744975] xhci_hcd 0000:04:00.3: WARNING: Host System Error
[ 8278.579462] ata1: SATA link up 6.0 Gbps (SStatus 133 SControl 300)
[ 8278.589589] ata1.00: configured for UDMA/133
[ 8278.599798] sd 0:0:0:0: [sda] Starting disk
[ 8395.536913] xhci_hcd 0000:04:00.3: remove, state 4
[ 8395.536931] usb usb2: USB disconnect, device number 1
[ 8395.537471] xhci_hcd 0000:04:00.3: USB bus 2 deregistered
[ 8395.537491] xhci_hcd 0000:04:00.3: WARNING: Host System Error
[ 8395.537522] xhci_hcd 0000:04:00.3: remove, state 1
[ 8395.537528] usb usb1: USB disconnect, device number 1
[ 8395.537531] usb 1-2: USB disconnect, device number 2
[ 8395.537533] usb 1-2.2: USB disconnect, device number 3
[ 8395.770224] usb 1-2.3: USB disconnect, device number 4
[ 8395.951265] xhci_hcd 0000:04:00.3: USB bus 1 deregistered
[ 8395.952587] xhci_hcd 0000:04:00.3: xHCI Host Controller
[ 8395.952603] xhci_hcd 0000:04:00.3: new USB bus registered, assigned bus number 1
[ 8395.953744] xhci_hcd 0000:04:00.3: new USB bus registered, assigned bus number 2
[ 8395.953751] xhci_hcd 0000:04:00.3: Host supports USB 3.1 Enhanced SuperSpeed
[ 8395.953879] usb usb1: New USB device found, idVendor=1d6b, idProduct=0002, bcdDevice= 5.19
[ 8395.953893] usb usb1: Product: xHCI Host Controller
[ 8395.953896] usb usb1: Manufacturer: Linux 5.19.10-1-default xhci-hcd
[ 8395.954190] hub 1-0:1.0: USB hub found
[ 8395.954218] hub 1-0:1.0: 4 ports detected
[ 8395.954935] usb usb2: We don't know the algorithms for LPM for this host, disabling LPM.
[ 8395.954990] usb usb2: New USB device found, idVendor=1d6b, idProduct=0003, bcdDevice= 5.19
[ 8395.955000] usb usb2: Product: xHCI Host Controller
[ 8395.955003] usb usb2: Manufacturer: Linux 5.19.10-1-default xhci-hcd
[ 8395.955479] hub 2-0:1.0: USB hub found
[ 8395.955504] hub 2-0:1.0: 4 ports detected
[ 8396.211467] usb 1-2: new high-speed USB device number 2 using xhci_hcd
[ 8396.361222] usb 1-2: New USB device found, idVendor=1a40, idProduct=0801, bcdDevice= 1.00
[ 8396.361239] usb 1-2: Product: USB 2.0 Hub
[ 8396.402399] hub 1-2:1.0: USB hub found
[ 8396.402670] hub 1-2:1.0: 4 ports detected
[ 8396.711800] usb 1-2.2: new full-speed USB device number 3 using xhci_hcd
[ 8396.856991] usb 1-2.2: New USB device found, idVendor=046d, idProduct=c24d, bcdDevice=80.01
[ 8396.857018] usb 1-2.2: Manufacturer: Logitech
"""
