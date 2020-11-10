
for sf_type in SF PtResolution PhiResolution EtaResolution
do
  for jet_type in AK4PFchs AK4PFPuppi AK8PFchs AK8PFPuppi
  do
      conddb --yes copy --destdb offline_data_jec.db  --to 307082 JR_dataRun2_RunABCD_25nsV1b_V3b_V7b_106X_DATA_${sf_type}_${jet_type} JR_dataRun2_Combined_UL_2017_2018_${sf_type}_${jet_type}
      conddb --yes copy --destdb offline_data_jec.db --from 307083 JR_Summer19UL18_JRV2_DATA_${sf_type}_${jet_type} JR_dataRun2_Combined_UL_2017_2018_${sf_type}_${jet_type}
  done
done

