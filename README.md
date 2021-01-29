# Zyxel NR7101 tool

## Installation

```sh
pip3 install git+https://github.com/pkorpine/nr7101.git
```

## Usage

```sh
nr7101-tool https://192.168.1.1 admin password
```

Note that by default the tool stores cookies to a file `.nr7101.cookie`. This can be changed with `--cookie`/`--no-cookie`.

## Example output

```
{'CELL_Roaming_Enable': False,
 'INTF_BSIC': 0,
 'INTF_CQI': 11,
 'INTF_Cell_ID': 2155551,
 'INTF_Current_Access_Technology': 'NR-NSA EN-DC',
 'INTF_Current_Band': 'LTE_BC28',
 'INTF_Downlink_Bandwidth': 3,
 'INTF_EcNo': -240,
 'INTF_IMEI': 'xxxxxxxxxxxxxx',
 'INTF_LAC': 0,
 'INTF_MCS': 14,
 'INTF_Module_Software_Version': 'RG502QEAAAR01A04M4G',
 'INTF_Network_In_Use': 'Current_FI DNA DNA_NR-NSA EN-DC_24412',
 'INTF_PMI': 20,
 'INTF_PhyCell_ID': 116,
 'INTF_RAC': 0,
 'INTF_RFCN': 9260,
 'INTF_RI': 1,
 'INTF_RSCP': -120,
 'INTF_RSRP': -94,
 'INTF_RSRQ': -11,
 'INTF_RSSI': -63,
 'INTF_SINR': 10,
 'INTF_Status': 'Up',
 'INTF_Supported_Bands': 'LTE_BC1,LTE_BC3,LTE_BC5,LTE_BC7,LTE_BC8,LTE_BC18,LTE_BC19,LTE_BC20,LTE_BC26,LTE_BC28,LTE_BC38,LTE_BC39,LTE_BC40,LTE_BC41,LTE_BC42',
 'INTF_TAC': 112,
 'INTF_Uplink_Bandwidth': 3,
 'NSA_Band': '',
 'NSA_Enable': True,
 'NSA_MCC': '244',
 'NSA_MNC': '12',
 'NSA_PCI': 116,
 'NSA_RFCN': 0,
 'NSA_RSRP': -106,
 'NSA_RSRQ': -12,
 'NSA_RSSI': -120,
 'NSA_SINR': 126,
 'Passthru_Enable': False,
 'Passthru_MacAddr': '',
 'Passthru_Mode': 'Dynamic',
 'SCC_Info': [],
 'USIM_ICCID': 'xxxxxxxxxxxx',
 'USIM_IMSI': 'xxxxxxxxxxxx',
 'USIM_PIN_Protection': False,
 'USIM_PIN_Remaining_Attempts': 3,
 'USIM_Status': 'DEVST_SIM_RDY'}
```
