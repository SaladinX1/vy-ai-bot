from vision.actions import click_text, type_text, wait_for_element

class FacebookPublisher:
    def publish_post(self, page_name, content):
        click_text("Pages")
        click_text(page_name)
        click_text("Create post")
        type_text(content)
        click_text("Publish")