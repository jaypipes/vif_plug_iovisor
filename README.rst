================
vif_plug_iovisor
================

An `os-vif` VIF plugin for plugging and unplugging virtual interfaces that use
PlumGrid's IOVisor technology stack.

Features
--------

* A `vif_plug_iovisor.iovisor.IovisorPlugin` VIF plugin for PlumGrid's IOVisor
  technology stack.

Installation
------------

Install the IOVisor VIF plugin using `pip`::

    sudo pip install vif_plug_iovisor

After doing so, the `os-vif` library's `initialize()` method will automatically
load the IOVisor VIF plugin in this library and allow Nova and any other
system to plug VIFs that use IOVisor technology in some capacity.

Configuration
-------------

The following configuration options are used by the
`vif_plug_iovisor.iovisor.IovisorPlugin` VIF plugin and are passed from the
`os_vif.initialize(**config)` function:

* `disable_rootwrap` -- Defaults to `False`. Override to entirely disable any
  use of rootwrap and instead rely solely on sudoers files.
* `use_rootwrap_daemon` -- Defaults to `False`. Override to enable the rootwrap
  daemon mode which can increase the performance of root-run commands.
* `rootwrap_config` -- Defaults to `'/etc/nova/rootwrap.conf'`. Path to the
  `oslo.rootwap` config file.
* `ovs_vsctl_timeout` -- Defaults to `120`. Number of seconds the `ovs-vsctl`
  program should wait before erroring out.
