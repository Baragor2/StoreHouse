from fastapi import HTTPException, status


class StoreHouseException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class NoSuchProductException(StoreHouseException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Такого продукта не существует"


class NotEnoughProductsException(StoreHouseException):
    status_code = status.HTTP_400_BAD_REQUEST


class NoSuchOrderException(StoreHouseException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Такого заказа не существует"
