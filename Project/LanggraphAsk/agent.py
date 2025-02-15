
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
import serpapi
import os
from dotenv import load_dotenv, find_dotenv
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import tools_condition, ToolNode
from langgraph.graph.state import CompiledStateGraph



load_dotenv()
open_api_key = os.getenv("OPENAI_API_KEY")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY") 
print(f"SERPAPI_API_KEY...",SERPAPI_API_KEY)

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o-mini", api_key=open_api_key)





class AgentState(MessagesState):
    # pass
    # messages: Annotated[List[Union[HumanMessage, AIMessage, SystemMessage]], operator.add]
    budget: float
    interests: List[str]
    companions: int
    city: List[str]
    days: int
    travel_date: str
    itinerary: List[dict]  # To store the final itinerary



class HotelsInput(BaseModel):
    q: str = Field(description='Location of the hotel')
    check_in_date: str = Field(description='Check-in date. The format is YYYY-MM-DD. e.g. 2024-06-22')
    check_out_date: str = Field(description='Check-out date. The format is YYYY-MM-DD. e.g. 2024-06-28')
    sort_by: Optional[str] = Field(8, description='Parameter is used for sorting the results. Default is sort by highest rating')
    adults: Optional[int] = Field(1, description='Number of adults. Default to 1.')
    children: Optional[int] = Field(0, description='Number of children. Default to 0.')
    rooms: Optional[int] = Field(1, description='Number of rooms. Default to 1.')
    hotel_class: Optional[str] = Field(
        None, description='Parameter defines to include only certain hotel class in the results. for example- 2,3,4')


class HotelsInputSchema(BaseModel):
    params: HotelsInput


@tool(args_schema=HotelsInputSchema)
def hotels_finder(params: HotelsInput):
    '''
    Find hotels using the Google Hotels engine.

    Returns:
        dict: Hotel search results.
    '''
    print(f"calling...")



    params = {
        'api_key': SERPAPI_API_KEY,
        'engine': 'google_hotels',
        'hl': 'en',
        'gl': 'pk',
        'q': params.q,
        'check_in_date': params.check_in_date,
        'check_out_date': params.check_out_date,
        'currency': 'PKR',
        'adults': params.adults,
        'children': params.children,
        'rooms': params.rooms,
        'sort_by': params.sort_by,
        'hotel_class': params.hotel_class
    }
    print(f"calling again...")

    search = serpapi.search(params)
    results = search.data
    print(f"hotels results",results)
    return results['properties'][:5]














class ImageSearchInput(BaseModel):
    q: str = Field(description="Search query for the image")
    safe: Optional[str] = Field(default="active", description="Safe search setting: active, moderate, or off")

# Define the tool without using args_schema
@tool
def image_finder(q: str, safe: str = "active") -> list:
    '''
    Find images using Google Images via SerpAPI.
    Args:
        q: Search query for the image
        safe: Safe search setting (active, moderate, or off)
    Returns:
        list: List of image results with URLs and metadata
    '''
    search_params = {
        "api_key": SERPAPI_API_KEY,
        "engine": "google_images",
        "q": q,
        "safe": safe,
        "hl": "en",
        "gl": "pk",
    }

    search = serpapi.search(search_params)
    results = search.data
    return results["images_results"][:10]








     


# LangChain Setup
def get_system_prompt(state: AgentState):
    return f"""You are a smart travel assistant. Create a detailed itinerary in JSON format considering:
    - Budget: PKR {state['budget']}
    - Travel Interests: {', '.join(state['interests'])}
    - Companions: {state['companions']} people
    - Destination: {state['city']}
    - Duration: {state['days']} days
    - Travel Date: {state['travel_date']}

    Use the hotels_finder tool to get hotel images and information. Use the image_finder tool to get high-quality images for Destination:{state['city']}.

    The response should be a valid JSON object with the following structure:
    {{
        "trip_details": {{
            "destination": string,
            "duration": number,
            "travel_date": string,
            "companions": number,
            "budget": number,  # in PKR
            "interests": string[]
        }},

        "destination_images": [
            {{
                "url": string,  # Only .jpg or .webp format images
            }}
        ],

        "hotel_images": [
            {{
                "url": string,  # Only .jpg or .webp format images
            }}
        ],

        "daily_itinerary": [
            {{
                "day": number,
                "date": string,
                "day_title": string,  # e.g., "Cultural Tour", "Arrival Day", "Adventure Day"
                "description": string,  # Brief description of the day's theme and activities
                "hotel": {{
                    "name": string,
                    "price": number,  # in PKR
                    "rating": number,
                    "reviews": number,
                    "booking_url": string
                    "image_url": string
                }},
                "transportation": {{
                    "type": string,
                    "cost": number  # in PKR
                }},
                "meals": [
                    {{
                        "type": string,
                        "venue": string,
                        "cost": number  # in PKR
                    }}
                ],
                "activities": [
                    {{
                        "name": string,
                        "description": string,
                        "cost": number,  # in PKR
                    }}
                ],
            }}
        ],

        "total_cost": number,  # in PKR
        "remaining_budget": number  # in PKR
    }}

    Instructions:
    1. Use image_finder to get 8-10 high-quality images of destination:{state['city']}.
    2. Include destination images in the destination_images array
    3. Include hotel images in the hotel_images array
    4. Ensure all image URLs are valid and accessible
    5. Only include images in .jpg or .webp format

    For each day:
    1. Provide a meaningful day_title that describes the theme (e.g., "Cultural Tour", "Adventure Day")
    2. Include a brief description explaining the day's focus and highlights

    In the cost_summary:
    1. Calculate the total trip cost in PKR
    2. Show the remaining budget from the original amount in PKR
    """


tools = [hotels_finder,image_finder]
llm_with_tools = llm.bind_tools(tools)

def assistant(state: AgentState)->AgentState:
    system_prompt = SystemMessage(content=get_system_prompt(state))
    print("state",[system_prompt] + state["messages"])
    return {"messages": [llm_with_tools.invoke([system_prompt] + state["messages"])]}


builder: StateGraph = StateGraph(AgentState)


builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))

# Define edges: these determine how the control flow moves
builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
    # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END
    tools_condition,
)
builder.add_edge("tools", "assistant")
graph: CompiledStateGraph = builder.compile()