class ZoomService:
    """
    Manages the application-wide view state for Zoom percentage.
    Responsible for bounding the zoom values (50% to 200%) and 
    dispatching formatting updates and UI status triggers.
    """
    
    MIN_ZOOM = 50
    MAX_ZOOM = 400
    ZOOM_STEP = 10
    
    def __init__(self, format_service=None, editor=None):
        """
        :param format_service: The FormatService to notify of zoom changes.
        :param editor: The Editor instance to trigger status bar updates.
        """
        self.format_service = format_service
        self.editor = editor
        self.current_percentage = 100
        
    def set_zoom(self, percentage: int):
        """Sets an explicit zoom percentage within bounds."""
        new_percentage = max(self.MIN_ZOOM, min(percentage, self.MAX_ZOOM))
        if new_percentage != self.current_percentage:
            self.current_percentage = new_percentage
            self._apply_zoom()

    def zoom_in(self):
        """Increases the zoom percentage by ZOOM_STEP."""
        new_percentage = min(self.current_percentage + self.ZOOM_STEP, self.MAX_ZOOM)
        if new_percentage != self.current_percentage:
            self.current_percentage = new_percentage
            self._apply_zoom()

    def zoom_out(self):
        """Decreases the zoom percentage by ZOOM_STEP."""
        new_percentage = max(self.current_percentage - self.ZOOM_STEP, self.MIN_ZOOM)
        if new_percentage != self.current_percentage:
            self.current_percentage = new_percentage
            self._apply_zoom()

    def reset_zoom(self):
        """Resets the zoom percentage to 100%."""
        if self.current_percentage != 100:
            self.current_percentage = 100
            self._apply_zoom()
            
    def get_zoom_percentage(self) -> int:
        """Returns the current zoom percentage."""
        return self.current_percentage
        
    def _apply_zoom(self):
        """Applies the current zoom to the format service and triggers a status update."""
        if self.format_service:
            self.format_service.set_zoom(self.current_percentage)
            
        if self.editor:
            self.editor.trigger_status_update()
