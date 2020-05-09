from typing import (
    TYPE_CHECKING,
    Iterable,
    Optional,
    Union,
)
from uuid import uuid4

from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    Float,
    DateTime,
    LargeBinary,
)
from sqlalchemy.orm import relationship

try:
    from apps.users import Base
    from apps.mixins.models import (SeoModel, PublishableModel,)
except ModuleNotFoundError as e: 
     # for alembic to work properly >> one dir up
    from src.apps.users import Base
    from src.apps.mixins.models import ( SeoModel, PublishableModel,)


class Category(SeoModel):
    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    slug = Column(String(255))
    description = Column(Text)
    parent = relationship('Category', remote_side=['id'], back_populates="children")
    background_image = Column(LargeBinary)
    background_image_alt = Column(String(128))
    products = relationship("Product")
    minimun_price_amount = Column(Float) 

    def __str__(self) -> str:
        return self.name


class Brand(SeoModel):
    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    slug = Column(String(255))
    description = Column(Text)
    background_image = Column(LargeBinary)
    background_image_alt = Column(String(128))
    products = relationship("Product")

    def __str__(self) -> str:
        return self.name


class ProductType(SeoModel):
    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    slug = Column(String(255))
    has_variants = Column(Boolean(), default=False)
    is_shipping_required = Column(Boolean(), default=True)
    is_digital = Column(Boolean(), default=False)
    weight = Column(String(20))
    products = relationship("Product")
    attributes = relationship("ProductAttribute")

    def __str__(self) -> str:
        return self.name


class Product(SeoModel, PublishableModel):
    id = Column(Integer, primary_key=True)
    product_type_id = Column(Integer, ForeignKey("producttype.id"))
    product_type = relationship("ProductType", back_populates="products")
    name = Column(String(250))
    slug = Column(String(255))
    description = Column(Text)
    category_id = Column(Integer, ForeignKey("category.id"))
    category = relationship( "Category", back_populates="products")
    brand_id = Column(Integer, ForeignKey("category.id"))
    brand = relationship("Brand", back_populates="products")
    price_amount = Column(Float) 
    images = relationship("ProductImage")
    variants = relationship("ProductVariant")
    attributes = relationship( 'ProductAttribute', back_populates="product", secondary='ProductAttributeValue')
    recommended_products = relationship('Product', secondary='ProductRecommendation')

    def __str__(self) -> str:
        return self.name


class ProductAttribute(SeoModel):
    id = Column(Integer, primary_key=True)
    product_type_id = Column(Integer, ForeignKey("producttype.id"))
    product_type = relationship("ProductType", back_populates="attributes")
    name = Column(String(128))
    code = Column(String(128))
    required = Column(Boolean, default=False)
    product_id = Column(Integer, ForeignKey("product.id"))
    product = relationship("Product")
    values = relationship("ProductAttributeValue")

    def __str__(self) -> str:
        return self.name
    

class ProductAttributeValue(Base):
    id = Column(Integer, primary_key=True)
    attribute_id = Column(Integer, ForeignKey("productattribute.id"))
    attribute = relationship('ProductAttribute', back_populates="values")
    product = relationship("Product")
    value = Column(String(100))

    def __str__(self) -> str:
        return self.value


class ProductRecommendation(Base):
    id = Column(Integer, primary_key=True)
    product = relationship("Product")
    product_id = Column(Integer, ForeignKey("product.id"))
    recommendation = relationship('Product', back_populates="recommended_products")

    def __str__(self) -> str:
        return "<. >"


class ProductImage(Base):
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("product.id"))
    product = relationship("Product", back_populates="images")
    image = Column(LargeBinary)
    alt = Column(String(128))

    def get_ordering_queryset(self):
        return self.product.images.all
    
    def __str__(self) -> str:
        return self.product.name + " <image alt:> " + self.alt


class ProductVariant(Base):
    id = Column(Integer, primary_key=True)
    sku = Column(String(255))
    name = Column(String(255))
    price_override_amount = Column(Float) 
    product_id = Column(Integer, ForeignKey("product.id"))
    product = relationship("Product", back_populates="variants")
    description = Column(Text)
    images = relationship("ProductImage", secondary="VariantImage")
    track_inventory = Column(Boolean(), default=False)
    digital_content = relationship("DigitalContent", uselist=False, back_populates="product_variant")
    old_price = Column(Float) 

    def __str__(self) -> str:
        return self.name or self.sku

    @property
    def is_visible(self) -> bool:
        return self.product.is_visible

    def get_weight(self):
        return self.weight or self.product.weight or self.product.product_type.weight

    def is_shipping_required(self) -> bool:
        return self.product.product_type.is_shipping_required

    def get_first_image(self) -> "ProductImage":
        images = list(self.images.all())
        return images[0] if images else self.product.get_first_image()


class VariantImage(Base):
    id = Column(Integer, primary_key=True)
    variant = relationship("ProductVariant", back_populates="variant_images")
    image = relationship("ProductImage", back_populates="variant_images")
    
    def __str__(self) -> str:
        return "<variant:> " + self.variant.name + " <image alt:> " + self.image.alt


class DigitalContent(Base):
    id = Column(Integer, primary_key=True)
    automatic_fulfillment = Column(Boolean(), default=False)
    product_variant_id = Column(Integer, ForeignKey("productvariant.id"))
    product_variant = relationship("ProductVariant", back_populates="digital_content")
    content_file = Column(LargeBinary)
    max_downloads = Column(Integer)
    url_valid_days = Column(Integer)

    def create_new_url(self) -> "DigitalContentUrl":
        return self.urls.create()

    def __str__(self) -> str:
        return self.product_variant.name

