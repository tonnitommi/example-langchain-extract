import json
from llm_call import call_openai

ECHO_USER_PROMPT = False
LLM_MODEL = "gpt-4"

PROMPT = """
Extract a standard JSON answer to gather data from the following discussion:
--DISCUSSION--

The response should be in the following JSON format and always in English:
{
--keys-and-values--
}
Please give only the JSON in the response:
"""


def extract_data_from_discussion(discussion: str, **kwargs) -> dict[str, str]:
    keys_and_values = "\n".join(f' "{k}": <{v}>' for k, v in kwargs.items())
    prompt = PROMPT.replace("--DISCUSSION--", discussion).replace(
        "--keys-and-values--", keys_and_values
    )
    response = call_openai(prompt, echo_user_prompt=True, echo_response=True, llm_model=LLM_MODEL)
    data = json.loads(response)
    return {key: data.get(key, "") for key in kwargs.keys()}

def run_extract():
    response_json = extract_data_from_discussion(
        """
Subject: Payment Confirmation for Invoice #13579 - Acme Industrial Appliances

Dear Rita,

We hope you are enjoying your recent purchase of our industrial appliances. We would like to remind you that your payment for Invoice #13579, dated 2023-04-12, is due next week Wed, on May 10th. Could you please confirm when we can expect the payment for this invoice?

Thank you for your prompt attention to this matter, and we look forward to hearing from you soon.

Best regards,
Björn Lund
Payment Collections Department
Acme Industrial Appliances

Dear Nalle,

We've already scheduled funds to be transferred next Monday!

Best regards,
Rita Hodges
Brewsters Brew Ltd.
""",
        invoice_id="id of the invoice in discussion",
        employee="full name of the employee in discussion",
        customer="full name of the customer in discussion",
        company="customer company name in the discussion",
        payment_date="date in ISO format that customer confirms as payment date for the invoice in the discussion. Leave empty if in the discussion the customer does not confirm their payment date. If customer asks for later payment date, insert that date here.",
        category="choose one of these five values: on-time if customer expects to pay on or before the due date, late if customer expects to pay after the due date, extend if customer asks for a later payment time, unknown if customer does not confirm their payment date or more-info if customer asks for more information about the invoice",
        summary="very short summary of the topic of the discussion",
    )

    try:
        print(json.dumps(response_json, indent=4))
    except TypeError:
        # If the response is not JSON, print it as is
        # This should only happen if the AI did not follow the instructions
        print(response_json)