import os
import logging
import asyncio

from PIL import Image

from src.db import async_session_maker_null_pool
from src.tasks.app import celery_app
from src.utils.db_manager import DBManager


@celery_app.task
def resize_image(image_path: str, output_folder: str, width_sizes: list[int]):
    logging.debug(
        f"Function 'resize_image' was invoked with args: {image_path=}, {output_folder=}, {width_sizes=}"
    )
    img = Image.open(image_path)
    base_name = os.path.basename(image_path)
    name, ext = os.path.splitext(base_name)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for width in width_sizes:
        resized_img = img.resize(
            (width, int(img.height * (width / img.width))), Image.Resampling.LANCZOS
        )

        new_file_name = f"{name}_{width}px{ext}"
        output_path = os.path.join(output_folder, new_file_name)
        resized_img.save(output_path)

    img.close()
    os.remove(image_path)
    logging.info(
        f"Image was resized to the following sizes: {width_sizes} and saved to {output_folder}"
    )


async def get_today_checkin():
    logging.info("Getting today checkin...")
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        bookings = await db.bookings.get_today_checkin()
        logging.info("Got today checkin: %s", bookings)


@celery_app.task(name="booking_today_checkin")
def send_emails_to_users_with_today_checkin():
    asyncio.run(get_today_checkin())
