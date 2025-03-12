from fastapi import APIRouter
from controllers.OfferController import addOffer, getOffers, updateOffer, deleteOffer
from models.OfferModel import Offer

router = APIRouter()

@router.post("/offer")
async def post_offer(offer: Offer):
    return await addOffer(offer)

@router.get("/offers")
async def get_all_offers():
    return await getOffers()


@router.put("/offer/{offer_id}")
async def put_offer(offer_id: str, offer: Offer):
    return await updateOffer(offer_id, offer)

@router.delete("/offer/{offer_id}")
async def delete_offer(offer_id: str):
    return await deleteOffer(offer_id)
