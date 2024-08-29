from typing import List
<<<<<<< HEAD
from fastapi import APIRouter, Depends, HTTPException, status
from auth.oauth2 import get_current_user
from db.db_conversation import get_conversations_for_user
from db.db_message import get_last_message_for_conversation
# from db.db_transaction import get_last_transaction_in_specific_conversation
from db.db_payment_request import get_last_payment_request_in_specific_conversation
from schemas import ConversationListDisplay, MessageDisplay, UserBase, UserDisplay
from db import db_user, models
=======
from fastapi import APIRouter, Depends
from schemas import UserAllDisplay, UserBase, UserDisplay
from db import db_user
>>>>>>> develop
from db.database import get_db
from sqlalchemy.orm import Session
from db.db_user import get_user
from db.db_reviews import get_filtered_reviews
import sys

sys.setrecursionlimit(10000)

router = APIRouter(
    prefix='/user',
    tags=['user']
)

# Create uer
@router.post('/', response_model=UserDisplay)
def create_user(request: UserBase, db: Session = Depends(get_db)):
    return db_user.create_user(db, request)

# Get all users
@router.get('/', response_model=List[UserAllDisplay])
def get_all_users(db: Session = Depends(get_db)):
    users: List[UserAllDisplay] = db_user.get_all_users(db)
    for user in users:
        average_rating = get_filtered_reviews(db, user.id)
        user.avarage_rating = average_rating
    return users
    
# Get user
@router.get('/{id}', response_model=UserDisplay)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db_user.get_user(db, id)
    average_rating = get_filtered_reviews(db, id)
    return UserDisplay(
        id=user.id,
        username=user.username,
        email=user.email,  
        avarage_rating=average_rating 
    )
    
# Update user
@router.put('/{id}/update')
def update_user(id: int, request: UserBase,  db: Session = Depends(get_db)):
    return db_user.update_user(db, id, request)

# Delete user
@router.delete('/delete/{id}')
def delete_user(id: int, db: Session = Depends(get_db)):
    return db_user.delete_user(db, id)

@router.get("/{user_id}/conversations", response_model=List[ConversationListDisplay])
def get_conversations(user_id: int, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):

    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this user's conversations."
        )    

    conversations = get_conversations_for_user(db, user_id)
    
    # Convert to a list of ConversationResponse objects, including the owner_id from the Product
    conversation_responses = []
    for conversation in conversations:
        # messages = get_messages_for_conversation(db, conversation.id)
        
        last_message = get_last_message_for_conversation(db, conversation.id)
        last_transaction = get_last_payment_request_in_specific_conversation(db, conversation.id)

        # message_displays = [MessageDisplay.model_validate(message) for message in messages]
        # transaction_displays = [TransactionDisplay.model_validate(transaction) for transaction in transactions]

        # conversation_responses.append(
        #     ConversationDisplay(
        #         id=conversation.id,
        #         advertisement_id=conversation.advertisement_id,
        #         buyer_id=conversation.buyer_id,
        #         seller_id=conversation.advertisement.owner_id,  # Access owner_id from the related product
        #         messages= message_displays,
        #         transactions=transaction_displays
        #     )
        # )

        conversation_responses.append(
            ConversationListDisplay(
                advertisement_title = conversation.advertisement.title,
                last_message_content = last_message.content[:50], # Truncate to 50 characters
                last_message_owner = last_message.sender_user_id,
                last_message_date = last_message.created_at,
                transaction_status = last_transaction.status if last_transaction else None,
            )
        )

    return conversation_responses
 