import re
import sentencepiece as spm
import pandas as pd

class Preprocessor:
    def __init__(self, file_path):
        self.df = pd.read_csv(file_path)
        
    def clean_vacant(self):
        for i, text in enumerate(self.df["comments"]):
            if text == "":
                self.df.drop([i], axis=0, inplace=True)
        return self.df
    
    def clean_text(self):
        for i, text in enumerate(self.df["comments"]):
            text = re.sub("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]", "", str(text))
            self.df["comments"][i] = text
        return self.df
            
    def labeling(self, criteria):
        labels = []
        for rating in self.df["ratings"]:
            label = 1 if rating >= criteria else 0
            labels.append(label)
        
        self.df["label"] = labels
        return self.df
    
    def preprocess_comments(self):
        processed_sentences = [self.clean_text(sentence) for sentence in self.sentences]
        return processed_sentences
    
    def tokenizer(self, data, vocab_size = 1500):
        comments = []
        for comment in data["comments"]:
            comments.append(comment)
        with open("comments.txt", "w", encoding="utf8") as f:
                f.write('\n'.join(self.df["comments"]))
        spm.SentencePieceTrainer.Train(
            f"--input=comments.txt \
            --model_prefix=tokenized \
            --pad_id=0  \
            --pad_piece=<pad> \
            --unk_id=1 \
            --unk_piece=<unk> \
            --bos_id=2 \
            --bos_piece=<s> \
            --eos_id=3 \
            --eos_piece=</s> \
            --vocab_size={vocab_size} \
            --model_type=bpe"
            )
        
        sp = spm.SentencePieceProcessor()
        vocab_file = "tokenized.model"
        sp.load(vocab_file)
        
        for i, comment in enumerate(data["comments"]):
            modified_comments = sp.encode_as_pieces(comment)
            data["comments"][i] = modified_comments
            
        return data
