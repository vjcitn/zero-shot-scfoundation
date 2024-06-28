
import os
import logging
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

from sc_foundation_evals import geneformer_forward as gf
from sc_foundation_evals import data, cell_embeddings, model_output
from sc_foundation_evals.helpers.custom_logging import log
log.setLevel(logging.INFO)

geneformer_data = "../data/weights/Geneformer"
# path to the pre-trained model, can work with the huggingface model hub
# i.e. ctheodoris/Geneformer
model_dir = os.path.join(geneformer_data, "default")
# path to dictionaries in geneformer repo
dict_dir = os.path.join(geneformer_data, "dicts")

# batch_size depends on available GPU memory
batch_size = 24
# output_dir is the path to which the results should be saved
output_dir = "../output/geneformer/6L/"
# path to where we will store the embeddings and other evaluation outputs
model_out = os.path.join(output_dir, "model_outputs")
# if you can use multithreading specify num_workers, -1 means use all available
num_workers = -1

# specify the path to anndata object
in_dataset_path = "../data/datasets/pancreas_scib.h5ad"
# dataset_name is inferred from in_dataset_path
dataset_name = os.path.basename(in_dataset_path).split(".")[0]
# specify the path for the output of the pre-processing
preprocessed_path = f"../data/datasets/geneformer/{dataset_name}/"
# create the preprocessed path if it does not exist
os.makedirs(preprocessed_path, exist_ok=True)
# in which column in adata.obs are gene names stored? if they are in index, the index will be copied to a column with this name
gene_col = "gene_symbols"
# batch column found in adata.obs
batch_col = "batch"
# where are labels stored in adata.obs? 
label_col = "celltype" #"str_labels"
# where the raw counts are stored?
layer_key = "counts" #"X" 

geneform = gf.Geneformer_instance(save_dir = output_dir, 
                                  saved_model_path = model_dir,
                                  explicit_save_dir = True,
                                  num_workers = num_workers)


# specify the path to anndata object
in_dataset_path = "../data/datasets/pancreas_scib.h5ad"
# dataset_name is inferred from in_dataset_path
dataset_name = os.path.basename(in_dataset_path).split(".")[0]
# specify the path for the output of the pre-processing
preprocessed_path = f"../data/datasets/geneformer/{dataset_name}/"
# create the preprocessed path if it does not exist
os.makedirs(preprocessed_path, exist_ok=True)
# in which column in adata.obs are gene names stored? if they are in index, the index will be copied to a column with this name
gene_col = "gene_symbols"
# batch column found in adata.obs
batch_col = "batch"
# where are labels stored in adata.obs? 
label_col = "celltype" #"str_labels"
# where the raw counts are stored?
layer_key = "counts" #"X" 


geneform = gf.Geneformer_instance(save_dir = output_dir, 
                                  saved_model_path = model_dir,
                                  explicit_save_dir = True,
                                  num_workers = num_workers)

geneform.load_pretrained_model()

geneform.load_vocab(dict_dir)

input_data = data.InputData(adata_dataset_path = in_dataset_path)

input_data.preprocess_data(gene_col = gene_col,
                           model_type = "geneformer",
                           save_ext = "loom",
                           gene_name_id_dict = geneform.gene_name_id,
                           preprocessed_path = preprocessed_path)

# run twice? if PosixPath error occurs?
geneform.tokenize_data(adata_path = os.path.join(preprocessed_path, 
                                                 f"{dataset_name}.loom"),
                       dataset_path = preprocessed_path,
                       cell_type_col = label_col)



geneform.extract_embeddings(data = input_data,
                            batch_size = batch_size, 
                            layer = -2)


eval_pred = model_output.GeneExprPredEval(geneform, 
                                          output_dir = model_out)

eval_pred.evaluate(n_cells = 500,
                   save_rankings = True)

eval_pred.visualize(n_cells = 100, cmap = "mako_r")

eval_ce = cell_embeddings.CellEmbeddingsEval(geneform,
                                             data = input_data,
                                             output_dir = model_out,
                                             label_key = label_col,
                                             batch_key = batch_col)
