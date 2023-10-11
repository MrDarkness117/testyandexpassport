class Verifier:
    """
    Проверяет данные, и выгружает лог
    """
    def __init__(self, logger, screenshot=None):
        self.logger = logger
        self.screenshot = screenshot

    def verify(self, description: str, condition):
        try:
            self.logger.log("Verify: " + description)
            assert condition
        except Exception as e:
            self.logger.log(f"ERROR: Verification fail! Screenshot saved: Log: {e}")
            self.screenshot()
