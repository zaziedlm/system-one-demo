import asyncio

from dotenv import load_dotenv
from typesafe_sdk import AsyncTypeSafeClient, Choice, Noul, Score

load_dotenv()


async def main() -> None:
    document = "二重に請求されました。至急修正してください。"
    #document = "二重に請求されるとか信じられません。お金のことなので謝罪してほしいし、今すぐ修正してください。"   
    #document = "二重に請求されているようなんです。急ぎませんが、修正していただけますか。"

    async with AsyncTypeSafeClient() as client:
        response = await client.system_one(
            state={"document": document},
            questions={
                "billing": Noul(instructions="このチケットは請求に関するものですか？"),
                "tone": Choice(
                    instructions="顧客はどのような口調ですか？",
                    criteria={"冷静": None, "いら立っている": None, "怒っている": None},
                ),
                "urgency": Score(
                    instructions="このチケットの緊急度はどの程度ですか？",
                    criteria=["待てる", "今週中", "今日中"],
                ),
            },
        )

    print("問い合わせ内容:",document)
    print(" > Noul - [請求に関するものか？] Yes / No:",response.nouls["billing"].noul)
    print(" > Choice - [口調] 冷静 / いら立っている / 怒っている:",response.choices["tone"].choice)
    print(" > Score - [緊急度] 待てる(0) / 今週中(1) / 今日中(2):",response.scores["urgency"].score)
    #print(response.answers)

if __name__ == "__main__":
    asyncio.run(main())
