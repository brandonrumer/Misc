$esxName = 'MyEsx'

$vmkName = 'vmk1'

$esx = Get-VMHost -Name $esxName

$esxcli = Get-EsxCli -VMHost $esx -V2

$if = $esxcli.network.ip.interface.ipv4.get.Invoke(@{interfacename=$vmkName})

$iArg = @{

    netmask = $if[0].IPv4Netmask

    type    = $if[0].AddressType.ToLower()

    ipv4    = $if[0].IPv4Address

    interfacename = $if[0].Name

    gateway = '192.168.10.222'

}

$esxcli.network.ip.interface.ipv4.set.Invoke($iArg)

$esxcli.network.ip.interface.ipv4.get.Invoke(@{interfacename=$vmkName})