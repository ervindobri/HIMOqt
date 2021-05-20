from PyQt6.QtWidgets import QLabel


class QStyles:
    primaryColor = "20c1dc"
    # font = QLabel('').font()

    # @staticmethod
    # def get_font(size):
    #     font = QLabel('').font()
    #     font.setPointSize(size)
    #     return font

    recordStyle = """
    QPushButton{
                background-color: white;
                color: #20c1dc;
                border: 2px solid red;
                border-radius: 7px;
            }
    """
    borderedStyle = """ 
            QWidget
            { 
                border: 1px solid #20c1dc;
                border-radius: 7px;
                background-color: #fefefe;
            }"""
    comboStyle = """
        QComboBox
        {
            background-color: white;
            border: 1px solid #20c1dc;
            border-radius: 7px;
        }
    """

    listStyle = """
        QListView{ 
            background-color: white; 
            border: none;
            border-radius: 7px;
        }
        QListView::item 
        {
            background-color: white;
            border: 1px solid #20c1dc;
            border-radius: 7px;
            margin: 5px;
            padding: 5px;
        }
        QListView::item:selected
        {
            background-color: #b8f5ff;
            color: #20c1dc;
        }
        
    """
    tabButtonStyle = """
        QToolButton
        {
            
        }
    """
    tabStyle = """
        QTabWidget {background-color: white; border: none;}
        QTabWidget::pane {
            border: none;
            background: white;
          }
        QTabBar {background-color: white;}
        QTabBar::tab:selected
        {
            color: #454545;
            background-color: white;
            font-weight: bold;    
            
            border-bottom: 4px solid #20c1dc;
        }
        QTabBar::tab
        {
            color: #bebebe;
            background-color: white;
            font-size: 13px;
            width: 80px;   
            text-align: left; 
        }
    """
    backgroundGrey = """
        QWidget
        {
            background-color: #f8f8f8;
            border-radius: 7px;
        }
    """
    backgroundWhite = """
            QWidget
            {
                background-color: white;
                border-radius: 7px;
            }
        """
    blue = "#20c1dc"
    darkBlue = "#20c1dc"
    styledButtonStyle = """
    QPushButton
        {
            background-color: #20c1dc;
            color: white;
            border: 1px solid #20c1dc;
            border-radius: 7px;
        }
    QPushButton:hover
    {
            background-color: #199fb5;
            color: white;
            border: 1px solid #20c1dc;
            border-radius: 7px;
    }
    """
    outlineButtonStyle = """
        QPushButton
            {
                background-color: white;
                color: #20c1dc;
                border: 1px solid #20c1dc;
                border-radius: 7px;
            }
            QPushButton:hover
    {
            background-color: white;
            font-weight: bold;
            border: 3px solid #20c1dc;
            border-radius: 7px;
    }
        """
    toolButtonStyle = """ QToolButton 
            {
                background-color: #20c1dc;
                color: white;
                border-radius: 7px;
                font-size: 16px;

            }
            """
    normalButtonStyle = """
    QPushButton
        {
            background-color: #20c1dc;
            color: white;
            border: 1px solid #20c1dc;
            border-radius: 7px;
        }
    """
    labelStyle = """
    QLabel
        {
            color: #555555;
            font-weight: bold;
        }
    """
    lineEditStyle = """
    QLineEdit
        {
            border: 1px solid #20c1dc;
            border-radius: 7px;
            padding: 10px;
        }
        """

