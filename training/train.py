import pandas as pd
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
from datasets import Dataset
from huggingface_hub import login
import os

data_file_name = "artclies"

# Load the CSV file and create a Huggingface Dataset
def csv_file_to_dataset(csv_file, save_to_disk=False):
    # Load your CSV file
    df = pd.read_csv(f"./data/training/{csv_file}.csv")

    # Filter necessary columns
    df = df[['text', 'tags']]

    # Create a Huggingface Dataset from the dataframe
    dataset = Dataset.from_pandas(df)

    # Split the dataset into training, validation and test sets
    temp_dataset = dataset.train_test_split(test_size=0.2, seed=42)
    train_dataset = temp_dataset['train']
    temp_dataset = temp_dataset['test'].train_test_split(test_size=0.5, seed=42)
    val_dataset = temp_dataset['train']
    test_dataset = temp_dataset['test']

    # Save the datasets to disk
    if save_to_disk:
        # Create the directory if it doesn't exist
        os.makedirs(f"./data/training/split/{csv_file}/", exist_ok=True)

        train_dataset.save_to_disk(f"./data/training/split/{csv_file}/train/")
        val_dataset.save_to_disk(f"./data/training/split/{csv_file}/eval/")

    datasets = {
        'train': train_dataset,
        'validation': val_dataset,
        'test': test_dataset
    }

    return datasets


# Load the datasets
datasets = csv_file_to_dataset(data_file_name, save_to_disk=False)

# Load the tokenizer and model (Log in to the Hugging Face Hub)
login(token="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")
tokenizer = AutoTokenizer.from_pretrained('meta-llama/Llama-2-7b-hf')
model = AutoModelForCausalLM.from_pretrained('meta-llama/Llama-2-7b-hf')

# Tokenize the dataset
def tokenize_function(examples):
    return tokenizer(examples['text'], padding='max_length', truncation=True)

tokenized_datasets = datasets.map(tokenize_function, batched=True)
print(tokenized_datasets["train"][0])

# Define training arguments
training_args = TrainingArguments(
    output_dir='./results',            # output directory
    num_train_epochs=3,                # number of training epochs
    per_device_train_batch_size=8,     # batch size for training
    per_device_eval_batch_size=32,     # batch size for evaluation
    warmup_steps=500,                  # number of warmup steps for learning rate scheduler
    weight_decay=0.01,                 # strength of weight decay
    logging_dir='./logs',              # directory for storing logs
    logging_steps=10,
    evaluation_strategy="steps",       # evaluate every logging_steps
    save_strategy="steps",             # save model every logging_steps
    save_total_limit=2,                # only keep the 2 most recent model checkpoints
)

# Initialize the Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=datasets['train'],
    eval_dataset=datasets['validation'],
    tokenizer=tokenizer,
)

# Start training
trainer.train()

# Evaluate the model on the test set
metrics = trainer.evaluate(eval_dataset=datasets['test'])
print(metrics)

# Make predictions on the test dataset
predictions, labels, _ = trainer.predict(datasets['test'])