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

# TODO: These imports reference the old structure and will need to be updated during migration
from window import MainWindow, FONT, get_fonts
from helpers import resource_path
from core.errors import log, log_exception


def setup_application_icon(app):
    """
    Set up the application icon with multiple sizes.
    
    Args:
        app (QApplication): The application instance to set the icon for
        
    If icon files are missing, the application will continue without an icon
    rather than crashing.
    """
    try:
        app_icon = QIcon()
        icon_sizes = [
            ('favicon/favicon-16x16.png', 16),
            ('favicon/favicon-24x24.png', 24),
            ('favicon/favicon-32x32.png', 32),
            ('favicon/favicon-48x48.png', 48),
            ('favicon/favicon-256x256.png', 256),
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


def setup_application_font(app):
    """
    Set up the default font for the application.
    
    Args:
        app (QApplication): The application instance to set the font for
        
    If font loading fails, the application will use the system default font.
    """
    try:
        # TODO: FONT and get_fonts need to be migrated from old structure
        font = get_fonts(FONT.text_small)
        app.setFont(font)
        log('DEBUG', 'Application font configured', category='main', action='setup_font')
        
    except Exception as e:
        log_exception(e, 'Failed to set application font', 
                     category='main', action='setup_font')
        # Continue with system default font - graceful degradation


def load_application_stylesheet(app):
    """
    Load and apply the QSS stylesheet for the application.
    
    Args:
        app (QApplication): The application instance to apply styles to
        
    If the stylesheet file is missing, the application will continue with
    default PyQt6 styling rather than crashing.
    """
    try:
        stylesheet_path = resource_path('styles/main.qss')
        
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


def create_and_show_main_window():
    """
    Create and display the main application window.
    
    Returns:
        MainWindow: The created main window instance, or None if creation failed
        
    If window creation fails, the application will log the error and return None.
    """
    try:
        # TODO: MainWindow needs to be migrated from old structure
        window = MainWindow()
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
        setup_application_icon(app)
        setup_application_font(app)
        load_application_stylesheet(app)
        
        # Create and show main window
        window = create_and_show_main_window()
        
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
