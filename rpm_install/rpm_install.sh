#!/bin/bash

hascli -ln /IWF-0/MGW_IWFMFU-0
echo fsswcli -pr tag:SS_MGWIWFConnMgr-trunk.*.rpm
fsswcli -pr tag:SS_MGWIWFConnMgr-trunk.*.rpm
echo fsswcli -pi @/x86_64/std_acpi5:$1
fsswcli -pi @/x86_64/std_acpi5:$1 | tee | grep 'patch(es) applied' 
if [ $? = 0 ]
then
    echo "Installation finished successfully!"
else
    echo "Installation failed, you must recover the environment manually!"
fi

hascli -un /IWF-0/MGW_IWFMFU-0

