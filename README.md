# Zyxel NR7101 tool

## Installation

```sh
pip3 install git+https://github.com/pkorpine/nr7101.git
```

## Usage

```sh
nr7101-tool https://192.168.1.1 admin password
```

Note that by default the tool stores cookies to a file `.nr7101.cookie`. The file can be specified with `--cookie`.
The cookie file can be disregarded with `--no-cookie`.

The tool can reboot the unit when the connection is down (i.e. `INTF_STATUS` ==
`Down`). Use `--reboot` to enable this feature. If you want to reboot the unit
regardless of the connection status, use `--force-reboot`.

The tool has an option to monitor given URLs and then issue a reboot. Use
`--monitor` to select this mode, and `-u` to define URLs to check. If none of
the URLs are reachable in the given period (`--monitor-threshold`), a reboot is
issued.

## Example output

```json
{
  "cellular": {
    "CELL_Roaming_Enable": false,
    "INTF_Status": "Up",
    "INTF_IMEI": "---",
    "INTF_Current_Access_Technology": "NR-NSA EN-DC",
    "INTF_Network_In_Use": "Current_DNA DNA_NR-NSA EN-DC_24412",
    "INTF_RSSI": -60,
    "INTF_Supported_Bands": "LTE_BC1,LTE_BC3,LTE_BC5,LTE_BC7,LTE_BC8,LTE_BC18,LTE_BC19,LTE_BC20,LTE_BC26,LTE_BC28,LTE_BC38,LTE_BC39,LTE_BC40,LTE_BC41,LTE_BC42",
    "INTF_Current_Band": "LTE_BC28",
    "INTF_Cell_ID": 123456,
    "INTF_PhyCell_ID": 123,
    "INTF_Uplink_Bandwidth": 3,
    "INTF_Downlink_Bandwidth": 3,
    "INTF_RFCN": 123,
    "INTF_RSRP": -88,
    "INTF_RSRQ": -12,
    "INTF_RSCP": -120,
    "INTF_EcNo": -240,
    "INTF_TAC": 112,
    "INTF_LAC": 0,
    "INTF_RAC": 0,
    "INTF_BSIC": 0,
    "INTF_SINR": 11,
    "INTF_CQI": 10,
    "INTF_MCS": 0,
    "INTF_RI": 1,
    "INTF_PMI": 20,
    "INTF_Module_Software_Version": "RG502QEAAAR01A04M4G",
    "USIM_Status": "DEVST_SIM_RDY",
    "USIM_IMSI": "---",
    "USIM_ICCID": "---",
    "USIM_PIN_Protection": false,
    "USIM_PIN_Remaining_Attempts": 3,
    "Passthru_Enable": false,
    "Passthru_Mode": "Dynamic",
    "Passthru_MacAddr": "",
    "NSA_Enable": true,
    "NSA_MCC": "244",
    "NSA_MNC": "12",
    "NSA_PCI": 116,
    "NSA_RFCN": 0,
    "NSA_Band": "",
    "NSA_RSSI": -120,
    "NSA_RSRP": -104,
    "NSA_RSRQ": -11,
    "NSA_SINR": 138,
    "SCC_Info": []
  },
  "traffic": {
    "br0": {
      "BytesSent": 2635510475,
      "BytesReceived": 1154508769,
      "PacketsSent": 5690109,
      "PacketsReceived": 6802894,
      "ErrorsSent": 0,
      "ErrorsReceived": 0,
      "UnicastPacketsSent": 0,
      "UnicastPacketsReceived": 0,
      "DiscardPacketsSent": 0,
      "DiscardPacketsReceived": 0,
      "MulticastPacketsSent": 0,
      "MulticastPacketsReceived": 0,
      "BroadcastPacketsSent": 0,
      "BroadcastPacketsReceived": 0,
      "UnknownProtoPacketsReceived": 0
    },
    "wwan0": {
      "BytesSent": 1731385995,
      "BytesReceived": 3287756124,
      "PacketsSent": 74133771,
      "PacketsReceived": 107353148,
      "ErrorsSent": 141,
      "ErrorsReceived": 0,
      "UnicastPacketsSent": 0,
      "UnicastPacketsReceived": 0,
      "DiscardPacketsSent": 0,
      "DiscardPacketsReceived": 0,
      "MulticastPacketsSent": 0,
      "MulticastPacketsReceived": 0,
      "BroadcastPacketsSent": 0,
      "BroadcastPacketsReceived": 0,
      "UnknownProtoPacketsReceived": 0
    },
    "wwan1": {
      "BytesSent": 0,
      "BytesReceived": 0,
      "PacketsSent": 0,
      "PacketsReceived": 0,
      "ErrorsSent": 0,
      "ErrorsReceived": 0,
      "UnicastPacketsSent": 0,
      "UnicastPacketsReceived": 0,
      "DiscardPacketsSent": 0,
      "DiscardPacketsReceived": 0,
      "MulticastPacketsSent": 0,
      "MulticastPacketsReceived": 0,
      "BroadcastPacketsSent": 0,
      "BroadcastPacketsReceived": 0,
      "UnknownProtoPacketsReceived": 0
    }
  }
}
```
