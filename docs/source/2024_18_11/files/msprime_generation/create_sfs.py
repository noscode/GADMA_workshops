import gadma
from gadma.data import VCFDataHolder

engine = gadma.get_engine("dadi")
data_holder = VCFDataHolder(vcf_file="fake_vcf.vcf", popmap_file="popmap")
data = engine.read_data(data_holder)
data.to_file("example_input_for_gadma.sfs")
