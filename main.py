"""
Main entry point for the StintFlow application.

This module initializes the PyQt6 application, sets up resources (icons, fonts, styles),
and launches the main window. All initialization is wrapped in error handling to ensure
graceful degradation if resources are missing or errors occur.
"""

import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize

from ui.components.window import ApplicationWindow
from ui.components import SettingsView
from ui.utilities import FONT, get_fonts
from core.utilities import resource_path
from core.errors import log, log_exception


def _setup_application_icon(app):
    """
    Set up the application icon with multiple sizes.
    
    If icon files are missing, the application will continue without an icon
    rather than crashing (graceful degradation).
    """
    try:
        app_icon = QIcon()
        icon_sizes = [
            ('resources/favicons/favicon-16x16.png', 16),
            ('resources/favicons/favicon-32x32.png', 32),
            ('resources/favicons/favicon-192x192.png', 192),
            ('resources/favicons/favicon-512x512.png', 512),
        ]
        
        for icon_path, size in icon_sizes:
            full_path = resource_path(icon_path)
            if Path(full_path).exists():
                app_icon.addFile(full_path, QSize(size, size))
            else:
                log('WARNING', f'Icon file not found: {icon_path}', 
                   category='main', action='setup_icon')
        
        app.setWindowIcon(app_icon)
        log('DEBUG', 'Application icon configured', category='main', action='setup_icon')
        
    except Exception as e:
        log_exception(e, 'Failed to set application icon', 
                     category='main', action='setup_icon')
        # Continue without icon - graceful degradation


def _setup_application_font(app):
    """
    Set up the default font for the application.
    
    If font loading fails, the application will use the system default font
    (graceful degradation).
    """
    try:
        font = get_fonts(FONT.text_small)
        app.setFont(font)
        log('DEBUG', 'Application font configured', category='main', action='setup_font')
        
    except Exception as e:
        log_exception(e, 'Failed to set application font', 
                     category='main', action='setup_font')
        # Continue with system default font - graceful degradation


def _load_application_stylesheet(app):
    """
    Load and apply the QSS stylesheet for the application.
    
    If the stylesheet file is missing, the application will continue with
    default PyQt6 styling (graceful degradation).
    """
    try:
        stylesheet_path = resource_path('resources/styles/main.qss')
        
        if not Path(stylesheet_path).exists():
            log('WARNING', f'Stylesheet file not found: {stylesheet_path}', 
               category='main', action='load_stylesheet')
            return
        
        with open(stylesheet_path, 'r', encoding='utf-8') as f:
            style = f.read()
            app.setStyleSheet(style)
        
        log('DEBUG', 'Application stylesheet loaded', category='main', action='load_stylesheet')
        
    except FileNotFoundError:
        log('WARNING', 'Stylesheet file not found, using default styling', 
           category='main', action='load_stylesheet')
    except Exception as e:
        log_exception(e, 'Failed to load application stylesheet', 
                     category='main', action='load_stylesheet')
        # Continue with default styling - graceful degradation


def _create_and_show_main_window():
    """
    Create and display the main application window.
    
    Returns:
        ApplicationWindow: The created main window instance, or None if creation failed
    """
    try:
        window = ApplicationWindow()
        window.show()
        log('INFO', 'Main window created and displayed', category='main', action='create_window')
        return window
        
    except Exception as e:
        log_exception(e, 'Failed to create main window', 
                     category='main', action='create_window')
        return None


def main():
    """
    Main entry point for the StintFlow application.
    
    Initializes the PyQt6 application, sets up resources (icons, fonts, styles),
    creates and displays the main window, and starts the event loop.
    
    All initialization steps include error handling to ensure the application
    degrades gracefully if resources are missing or errors occur.
    """
    try:
        # Create application instance
        app = QApplication(sys.argv)
        log('INFO', 'Application instance created', category='main', action='startup')
        
        # Set application style
        app.setStyle('Fusion')
        log('DEBUG', 'Application style set to Fusion', category='main', action='startup')
        

        # Set up application resources
        _setup_application_icon(app)
        _setup_application_font(app)
        _load_application_stylesheet(app)
        
        # Create and show main window
        window = _create_and_show_main_window()
        
        if window is None:
            log('ERROR', 'Failed to create main window, exiting', 
               category='main', action='startup')
            return 1


        # Start event loop
        log('INFO', 'Starting application event loop', category='main', action='startup')
        exit_code = app.exec()
        
        log('INFO', f'Application exiting with code: {exit_code}', 
           category='main', action='shutdown')
        return exit_code
        
    except Exception as e:
        log_exception(e, 'Fatal error during application startup', 
                     category='main', action='startup')
        return 1


if __name__ == '__main__':
    sys.exit(main())
