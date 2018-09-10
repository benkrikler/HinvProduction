#!/bin/bash
ScriptDir="$(readlink -f "$(dirname "${BASH_SOURCE[0]}")")"
echo $ScriptDir
ProdMode="$1" ; shift
BuildDir="$1"
if [ -z "$ProdMode" ] ; then
    echo "No Higgs production mode given"
    exit 1
elif  [ "${ProdMode^^}" != WPLUSH -a "${ProdMode^^}" != WMINUSH -a "${ProdMode^^}" != ZH ];then
    echo "No valid gridpack for $ProdMode"
    exit 1
fi

BuildDir="$(readlink -f "${BuildDir:-build_$ProdMode}")"
mkdir -p "$BuildDir"
cd "$BuildDir"

voms-proxy-init --voms cms -rfc

CrabCfgDir=crab_cfgs
[ -d "$BuildDir/$CrabCfgDir" ] || mkdir "$BuildDir/$CrabCfgDir"
(
cd "$ScriptDir/$CrabCfgDir"
Kernel="${ProdMode}_Vhadronic_Hinv_M125"
for cfg in *.py ;do 
    Step="$(sed -e 's/crab_submission_\(.*\)\.py/\1/' <<< $cfg)"
    DriverCfg="$BuildDir/driver_cfg_${Step}.py"
    echo Crab config: $cfg
    echo Step: $Step
    echo CMS Driver config: $DriverCfg
    sed -e 's!%%KERNEL%%!'"$Kernel"'!g' -e 's!%%DRIVER%%!'"$DriverCfg"'!g' "$cfg"  > "$BuildDir/$CrabCfgDir/$cfg"
done
)
