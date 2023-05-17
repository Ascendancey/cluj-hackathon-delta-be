import dataclasses
from enum import StrEnum
import os

import openai


class Role(StrEnum):
    SYSTEM = 'system',
    ASSISTANT = 'assistant',
    USER = 'user',


@dataclasses.dataclass
class Prompt:
    role: Role
    content: str

    def to_object(self):
        return {"role": self.role, "content": self.content}


def authenticate():
    openai.api_key = os.getenv("OPENAPI_KEY")


def get_available_products() -> [str]:
    products = []
    print(os.listdir('./Delta'))
    for filename in os.listdir('./Delta'):
        file_path = os.path.join('./Delta', filename)
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding="utf-8") as file:
                content = file.read()
                products.append(content)
    return products


def ask(available_products, question):
    prompts = [
        Prompt(role=Role.SYSTEM,
               content="You are a sales assistant which helps the customer to decide what washing machine to buy. Answer as concisely as possible.").to_object(),
        Prompt(role=Role.USER,
               content="Suggest only the washing machines provided in the following prompts. You will not have knowledge of any other washing machines. Suggest only the best fit and give a short reason and then the link to the onlineshop.").to_object(),
        Prompt(role=Role.USER,
               content="Remember a top-loading machine is great if you do not want to bend down so far.").to_object()
    ]
    prompts.extend(
        map(lambda p: Prompt(role=Role.USER, content=p).to_object(), available_products))
    prompts.append(
        Prompt(role=Role.USER,
               content=question).to_object()
    )
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=prompts
    )
    return res


def main():
    authenticate()
    question = "List all washing machines that have been provided to you with a link to the onlineshop"
    question = "I want a washing machine where I don't have to bend down so far because of my back"
    question = "I want a cheap washing machine"
    response = ask(get_available_products(), question)
    print(response)


if __name__ == '__main__':
    main()
