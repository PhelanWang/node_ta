# coding: utf-8
from agent_disk_scan import my_vdisk_scan, my_disk_scan, my_erase_scan
from agent_mmount import mmount_test
from agent_nfs import my_nfs
from agent_spice import spice
from agent_unsecurity_service import my_unsecurity_service_testing
from agent_vnc import vnc
from agent_vnic import vnic_analysis
from agent_quick_flaw_scan import my_quick_kvmflaw_scan, my_quick_ovirtflaw_scan, my_quick_VDSMflaw_scan, my_quick_libvirtflaw_scan


if __name__ == '__main__':
    my_quick_libvirtflaw_scan(0, 0)