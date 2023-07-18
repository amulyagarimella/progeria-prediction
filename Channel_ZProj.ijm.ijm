// code to split channel and calculate MIP for each channel
setBatchMode(true);

function splitchannel_mip (dir1, dir2) {
	list = getFileList(dir1);
	print(list.length);
	
	for (i=0; i < list.length; i++) {
		showProgress(i+1, list.length);
		fname = list[i];
		print(fname);
		if (!(fname.endsWith(".ims"))) {
			continue;
		}
		
		// ensure multichannel
		run("Bio-Formats", "open=[" + dir1 + fname + "] autoscale color_mode=Default rois_import=[ROI manager] view=Hyperstack stack_order=XYCZT series_1");
		getDimensions(width, height, channels, slices, frames);
		if (channels < 2) {
			print("not multichannel");
			continue;
		}
		
		print("Splitting...");
		run("Split Channels");
		
		imageList = getList("image.titles");
		
		for (j=0; j < imageList.length; j++) {
			showProgress(j+1, imageList.length);
			title = imageList[j];
			print(title);
			selectImage(title);
			getDimensions(width, height, channels, slices, frames);
			if (slices < 2 && frames < 2) {
				saveAs("Tiff", dir2 + fname.substring(0,fname.length-4) + "_" + title.substring(0,2) + ".tif");
				close();
				print("done");
			} 
			else {
				run("Z Project...", "projection=[Max Intensity] all");
				saveAs("Tiff", dir2 + fname.substring(0,fname.length-4) + "_" + title.substring(0,2) + "_max_proj.tif");
				close();
				close();
				print("done");
			}
			
		}
	
	}
	print("complete");
}

progeria_dirs = newArray("Y:/users/IGS/Experiments/Expt28_IF For NP_P22_P25 progeria/Passage 22 Progeria/PostEX_P22progeria_IF_DAPI_LMNA_Nup_LMNB1_0.2/", "Y:/users/Ajay/New progeria lines IF/Progerin_LMNA_K9ME2_K9ME4/2023-01-19/", "Y:/users/Ajay/IF_Progeria1972/Late_passage/2023-02-07/");
normal_dirs = newArray("Y:/users/IGS/Experiments/Expt28_IF For NP_P22_P25 progeria/Normal Progeria/PostEX_NP_IF_Progerin_LMNA_Nup_LMNB1/", "Y:/users/IGS/Experiments/Expt28_IF For NP_P22_P25 progeria/Normal Progeria/PostEX_NP_IF_LMNA_K9me2_K9me3/", "Y:/users/Ajay/IF_Progeria1972/Normal fibroblast/2023-02-10/");

dir2_p = "Y:/users/Amulya/converted_v2/progeria/"
dir2_n = "Y:/users/Amulya/converted_v2/normal/"

//for (p=0; p < progeria_dirs.length; p++) {
//	splitchannel_mip(progeria_dirs[p], dir2_p);
//}

for (n=1; n < normal_dirs.length; n++) {
	splitchannel_mip(normal_dirs[n], dir2_n);
}

print("all files converted");