import QtQuick
import QtQuick.Controls
import QtQuick.Window
import QtQuick.Layouts
import RinUI


FluentPage{
    title: qsTr("关于")
    ColumnLayout{
        spacing:10
        SettingCard{
            Layout.fillWidth: true
            icon: "ic_fluent_info_20_regular"
            title: "使用敬告"
            description: qsTr("本软件仅用于您了解破解极域/锐捷集控程序的原理，请勿用于教育环境，否则您可能会收到贵校老师温柔的抚摸（划掉）")
        }

        SettingExpander {
            Layout.fillWidth: true
            icon.name: "ic_fluent_info_20_regular"
            title: qsTr("关于")
            description: qsTr("查看作者与本软件的版本号")
            expanded: true
            SettingItem {
                title: qsTr("版本")
                description: qsTr("本软件的版本号")
                Text{
                    text: qsTr("V 0.9BETA(内部开发版本：NEXT-0.5)") 
                }
            }
            SettingItem{
                title:qsTr('内核版本')
                description: qsTr('当前使用的ITLT内核版本')
                Text{
                    text: qsTr("Next-0.5-Dev(技术预览版：0.5.1.2026130)") 
                }
            }
            SettingItem {
                title: qsTr("查看常用链接")
                description: qsTr("查看本软件的GitHub开源项目地址、官网、QQ群")
                Hyperlink {
                    text: qsTr("官网")
                    openUrl: "https://itltoolkit.great-site.net/"
                }
                Hyperlink {
                    text: qsTr("Github(给个Star呗)")
                    openUrl: "https://github.com/denjehdhuendx/itltoolkit-project"
                }
                Hyperlink {
                    text: qsTr("QQ群（1046723529）")
                    openUrl: "https://qm.qq.com/q/f2mbKV9t28"
                }
            }
            SettingItem{
                title:qsTr('作者')
                description: qsTr('Copyright©️2025-2026 MR-SHUIJIAO')
                Hyperlink{
                    text: qsTr('哔哩哔哩空间')
                    openUrl: 'https://space.bilibili.com/3493130934422121?spm_id_from=333.1007.0.0'
                }   
            }
        }
        SettingExpander { 
            Layout.fillWidth: true
            icon.name: "ic_fluent_apps_20_regular"
            title:qsTr('第三方库')
            description: qsTr("查看本软件开发过程中所使用的第三方库")
            expanded: true
            SettingItem{
                title:qsTr('Python')
                description: qsTr('Python 3.13.0')
            }
            SettingItem{
                title:qsTr('Pyside6')
                description: qsTr('PySide6 6.6.1')
            }
            SettingItem{
                title:qsTr('QtQuick')
                description: qsTr('QtQuick 2.15.13')
            }
            SettingItem{
                title:qsTr('RinUI')
                description: qsTr('Copyright © 2025 RinLit')
                Hyperlink{
                    text: qsTr('文档')
                    openUrl: 'https://ui.rinlit.cn/zh/'
                }
            }
            SettingItem{
                title:qsTr('虚位以待')
                description: qsTr('等待其他第三方库的加入...')
                
            }
        }
        SettingExpander{
            Layout.fillWidth: true
            icon.name: "ic_fluent_accessibility_question_mark_20_regular"
            title:qsTr('鸣谢')
            description:qsTr('感谢以下开发者对本项目的支持与贡献')
            expanded: true
            SettingItem{
                title:qsTr('MR-SHUIJIAO')
                description:qsTr('主开发，写代码巨水（')
                Hyperlink{
                    text: qsTr('哔哩哔哩空间')
                    openUrl: 'https://space.bilibili.com/3493130934422121?spm_id_from=333.1007.0.0'
                }   

            }
            SettingItem{
                title:qsTr('是星星与然然呀')
                description:qsTr('同样初一（测试）')
                Hyperlink{
                    text: qsTr('哔哩哔哩空间')
                    openUrl: 'https://space.bilibili.com/1532090388'
                }   
            }
        }
    }
}