FILES = build_vio_Mean.ps\
				build_vio_RMS.ps\
				bus_lic_Mean.ps\
				bus_lic_RMS.ps\
				chi_crime_Mean.ps\
				chi_crime_RMS.ps\
				contracts_Mean.ps\
				contracts_RMS.ps\
				graf_rmv_Mean.ps\
				graf_rmv_RMS.ps\
				unified_Mean.ps\
				unified_RMS.ps


all: $(patsubst %.ps,%.pdf,${FILES})

png: $(patsubst %.ps,%.png,${FILES})

draw: 
	python3 draw.py 

%.pdf : %.ps 
	ps2pdf $< 

%.png : %.pdf
	convert $< $*.png

.PHONY: all draw png