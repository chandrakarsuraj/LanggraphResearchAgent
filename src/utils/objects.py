from pydantic import BaseModel , Field
from typing import List


# creating our object Analyst
class Analyst(BaseModel):
    affilition: str = Field(description="The organization, institution, or company the analyst is affiliated with.")
    name: str = Field(description="The analyst's full name.")
    role: str = Field(description="The analyst's professional role or area of responsibility.")
    description: str = Field(description="A concise summary of the analyst's expertise, perspective, and relevant background.")


    @property
    def persona(self)->str:
        return f"Name : {self.name}\nRole: {self.role}\nAffilition: {self.affilition}\nDescription: {self.description}"


class Perspective(BaseModel):
    analysts: List[Analyst] = Field(description="A list of analyst personas to consult, each representing a distinct area of expertise or viewpoint for the research.")



class SearchQuery(BaseModel):

    search_query: str = Field(description="Search query for retrivel")
    