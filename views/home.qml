import QtQuick
import QtQuick.Controls
import QtQuick.Window
import QtQuick.Layouts
import RinUI


FluentPage {
    title: qsTr("首页")
    ColumnLayout{
        spacing:10
        SettingCard{
            Layout.fillWidth: true
            title:qsTr('打开反集控页面')
            description: qsTr("点击打开反集控功能页面")
            Button{
                text: qsTr('点击立即去')
            }
        }
        
    }
}