from transformers import ReformerModelWithLMHead, ReformerTokenizer, ReformerConfig
from NeuralNetworks.core.machine import SequenceToSequenceEngine
from transformers import Trainer, TrainingArguments, DataCollatorForLanguageModeling
from Utils.custom_tokenizers import BPE_tokenizer
from transformers import PreTrainedTokenizer
from NeuralNetworks.core.nn_dataset import TensorTokenSet

class MyTokenizer(ReformerTokenizer):
    
    def __init__(self, bpe_tokenizer):
        self.sp_model = bpe_tokenizer.sp
        PreTrainedTokenizer.__init__(self)
        self.add_special_tokens({'pad_token':'<PAD>',
                                 'unk_token':'<UNK>',
                                 'mask_token':'<MASK>'})
        
    def __repr__(self):
        return "SentencePieceTokenizer(vocab size = {})".format(self.vocab_size)


class ReformerLanguageEngine(SequenceToSequenceEngine):

    def __init__(self, **kwargs):
        
        config = ReformerConfig(max_position_embeddings = 1024,
                                axial_pos_shape = [32,32],
                                vocab_size=8000,
                                is_decoder=True,
                                num_buckets=32)
        self.model = ReformerModelWithLMHead(config)
        self.model.cpu()
    
    
    def fit(self, dataset):
        
        self.training_args = TrainingArguments(output_dir = "c:/models/reformer", 
                                               no_cuda = False,
                                               
                                               num_train_epochs = 20.0)
        bpe_tok = BPE_tokenizer(vocab_size = 8000)
        bpe_tok.fit(dataset)
        self.tokenizer = MyTokenizer(bpe_tok)
        tokenset = TensorTokenSet(dataset, self.tokenizer)
        self.data_collator = DataCollatorForLanguageModeling(tokenizer = self.tokenizer,
                                                             mlm = False,
                                                             mlm_probability = 0.15)
        self.trainer = Trainer(model=self.model,
                               args=self.training_args,
                               data_collator=self.data_collator,
                               train_dataset=tokenset)
        self.trainer.train()

    def save(self,path):
        pass
    
    def load(self,path):
        pass

        
from Utils.fileaccess import Fast_File



ff = Fast_File()
ff.load("c:/data/corpus/new-2.ff.npy")
#m = ReformerLanguageEngine()
#m.fit(ff)