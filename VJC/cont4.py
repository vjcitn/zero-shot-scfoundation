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
