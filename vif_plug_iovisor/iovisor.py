#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from os_vif import plugin
from os_vif import objects

from vif_plug_ovs import processutils
from vif_plug_ovs import linux_net

PLUGIN_NAME = 'iovisor'


class IovisorPlugin(base.PluginBase):
    """A VIF type that plugs into a PLUMgrid virtual domain."""

    def __init__(self, **config):
        processutils.configure(**config)

    def get_supported_vifs(self):
        return set([objects.PluginVIFSupport(PLUGIN_NAME, '1.0', '1.0')])

    def plug(self, instance, vif):
        """Plug using PLUMgrid IO Visor Driver

        Connect a network device to their respective
        Virtual Domain in PLUMgrid Platform.
        """
        dev = vif.devname
        iface_id = vif.id
        linux_net.create_tap_dev(dev)
        net_id = vif.network.id
        tenant_id = instance.project_id
        processutils.execute('ifc_ctl', 'gateway', 'add_port', dev,
                             run_as_root=True)
        processutils.execute('ifc_ctl', 'gateway', 'ifup', dev,
                             'access_vm',
                             vif.network.label + "_" + iface_id,
                             vif.address, 'pgtag2=%s' % net_id,
                             'pgtag1=%s' % tenant_id,
                             run_as_root=True)

    def unplug(self, vif):
        """Unplug using PLUMgrid IO Visor Driver

        Delete network device and to their respective
        connection to the Virtual Domain in PLUMgrid Platform.
        """
        iface_id = vif.id
        dev = vif.devname
        processutils.execute('ifc_ctl', 'gateway', 'ifdown', dev, 'access_vm',
                              vif.network.label + "_" + iface_id, vif.address,
                              run_as_root=True)
        processutils.execute('ifc_ctl', 'gateway', 'del_port', dev,
                             run_as_root=True)
                      
        linux_net.delete_net_dev(dev)
