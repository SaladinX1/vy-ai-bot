from vision.actions import click_text, type_text, wait_for_element


class InstagramBot:
    def post_reel(self, video_path, caption):
        click_text("+ Create")
        click_text("Reel")
        type_text(video_path)
        type_text(caption)
        click_text("Share")