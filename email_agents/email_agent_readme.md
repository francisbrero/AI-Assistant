# What does this agent do?

You can train the agent to recognize important emails and draft responses using the following command:

```bash 
python main.py -model gpt-4o -training
```

NB: When you are testing the system, we highly recommend using a cheap model such as 4o mini. You should ensure you have these models configured in your OAI_CONFIG file.
For reference: (Model, input, output)

- gpt-4o $2.50 / 1M input tokens $1.25 / 1M input tokens
- gpt-4o-mini $0.150 / 1M input tokens $0.075 / 1M input tokens
- gpt-3.5-turbo-0125 $0.50 / 1M tokens $1.50 / 1M tokens
- gpt-4-turbo: $10.00 / 1M tokens $30.00 / 1M tokens

```bash 
python main.py -model gpt-4o-mini -training
```

To run the email agent, use the following command:

```bash
python main.py -agent email
```

The email agent is a conversational agent that can be trained to recognize important emails and draft responses. The agent uses the OpenAI API to generate responses based on the input email and the training data provided.

# How to use the email agent

To train the email agent, you can use the following command:

```bash
python main.py -model gpt-4o-mini -training
```

When testing the system, it is recommended to use a cheaper model such as `gpt-4o-mini`. You can configure the models in the `OAI_CONFIG` file.

To stop the training process, enter `exit`.