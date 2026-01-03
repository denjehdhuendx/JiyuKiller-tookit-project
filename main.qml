import QtQuick
import QtQuick.Controls
import QtQuick.Window
import RinUI  // 仅需在您现有的项目中导入本库


FluentWindow {
    width: 1600
    height: 900
    visible: true
    title: qsTr("ITLToolkit Next")
    icon: "next.png"
    

    
    navigationItems: [
        {
            title: qsTr("首页"),
            page: Qt.resolvedUrl("views/home.qml"),
            icon: "ic_fluent_home_20_regular"
        },
        
        {
            title: qsTr("关于"),
            page: Qt.resolvedUrl("views/about.qml"),
            icon: "ic_fluent_info_20_regular"
        }
        
    ]
}