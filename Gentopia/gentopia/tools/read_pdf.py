from typing import AnyStr
import io
import requests as req
from pypdf import PdfReader
from gentopia.tools.basetool import *


class ReaderArgs(BaseModel):
    path: str = Field(..., description="a pdf path")


class ReadPDF(BaseTool):
    """Tool that adds the capability to read the contents of a PDF given it's URL."""

    name = "read_pdf"
    description = ("A parser retrieving the text from a PDF."
                   "Input should be a URL path of a PDF.")

    args_schema: Optional[Type[BaseModel]] = ReaderArgs

    def _run(self, path: AnyStr) -> str:
        res = req.get(path, timeout=95)
        reader = PdfReader(io.BytesIO(res.content))
        pageContent = '\n\n'
        for page_index in range(len(reader.pages)):
            if(not len(pageContent) >= 16300):
                page = reader.pages[page_index]
                pageContent += page.extract_text()
        return pageContent

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


if __name__ == "__main__":
    ans = GoogleSearch()._run("Attention for transformer")
    print(ans)
