import os
import sys
import psutil
import subprocess
import time
import winreg
import shutil
import ctypes

# ==================== 实用函数区域 (前面已详细说明，此处仅作引用) ====================
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    if not is_admin():
        print("警告：当前非管理员权限。尝试以管理员权限重新启动脚本...")
        # Get path to Python executable
        python_exe = sys.executable
        # Pass the current script path as argument to the new admin process
        script_path = os.path.abspath(__file__)
        
        try:
            # ShellExecuteW parameters: hwnd, lpOperation, lpFile, lpParameters, lpDirectory, nShowCmd
            # "runas" requests elevation
            ctypes.windll.shell32.ShellExecuteW(None, "runas", python_exe, f'"{script_path}"', None, 1)
        except Exception as e:
            print(f"错误：无法以管理员权限启动。请手动右键以管理员身份运行此脚本。")
            print(f"详细错误: {e}")
        sys.exit(0) # 退出当前非管理员进程

def find_jiyu_processes():
    # ... (与上面相同的实现) ...
    jiyu_keywords = ['studentmain.exe', 'client.exe', 'ggbrowser.exe', 'gknetlock.exe', 'gknetlocksvc.exe'] # 常见极域进程名，需根据实际情况补充
    found_processes = []
    for proc in psutil.process_iter(['pid', 'name', 'exe', 'cmdline', 'username']):
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name', 'exe', 'cmdline', 'username'])
            process_name_lower = pinfo['name'].lower()
            if any(keyword in process_name_lower for keyword in jiyu_keywords):
                found_processes.append(pinfo)
            if pinfo['cmdline']:
                cmdline_str = " ".join(pinfo['cmdline']).lower()
                if "jiyu" in cmdline_str or "guardking" in cmdline_str:
                    if pinfo not in found_processes:
                        found_processes.append(pinfo)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return found_processes

def find_jiyu_services():
    # ... (与上面相同的实现) ...
    jiyu_keywords = ['guardking', 'jiyu', 'studentdesktop', 'studentcontrol']
    try:
        result = subprocess.run(['sc', 'query', 'type= service', 'state= all'], capture_output=True, text=True, check=True, encoding='gbk')
        services_output = result.stdout
        
        found_services = []
        current_service = {}
        for line in services_output.splitlines():
            line = line.strip().lower()
            if line.startswith("service_name:"):
                if current_service:
                    found_services.append(current_service)
                current_service = {"name": line.split(":")[1].strip(), "display_name": "", "state": "", "binary_path": ""}
            elif line.startswith("display_name:"):
                current_service["display_name"] = line.split(":")[1].strip()
            elif line.startswith("state:"):
                current_service["state"] = line.split(":")[2].strip().split()[0]
            elif line.startswith("binary_path_name:"):
                current_service["binary_path"] = line.split(":")[1].strip()

        if current_service:
            found_services.append(current_service)

        jiyu_services = []
        for svc in found_services:
            if any(keyword in svc['name'] for keyword in jiyu_keywords) or \
               any(keyword in svc['display_name'] for keyword in jiyu_keywords) or \
               any(keyword in svc['binary_path'] for keyword in jiyu_keywords):
                jiyu_services.append(svc)
        return jiyu_services

    except subprocess.CalledProcessError as e:
        print(f"查询服务失败: {e}")
        return []

def find_jiyu_registry_entries():
    # ... (与上面相同的实现) ...
    jiyu_keywords = ['guardking', 'jiyu', 'topdomain', 'studentmain']
    run_keys = [
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"),
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce"),
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce"),
    ]
    found_entries = []

    for hkey, subkey_path in run_keys:
        try:
            with winreg.OpenKey(hkey, subkey_path, 0, winreg.KEY_READ) as key:
                i = 0
                while True:
                    try:
                        name, value, type = winreg.EnumValue(key, i)
                        value_str = str(value).lower()
                        if any(keyword in value_str for keyword in jiyu_keywords):
                            found_entries.append(f"{hkey}\\{subkey_path}\\{name} = {value}")
                        i += 1
                    except OSError:
                        break
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"读取注册表键 {subkey_path} 失败: {e}")
    
    # 广度搜索 SOFTWARE 键下可能的极域相关子键
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE", 0, winreg.KEY_READ) as software_key:
            i = 0
            while True:
                try:
                    sub_key_name = winreg.EnumKey(software_key, i)
                    if any(keyword in sub_key_name.lower() for keyword in jiyu_keywords):
                        found_entries.append(f"HKEY_LOCAL_MACHINE\\SOFTWARE\\{sub_key_name}")
                    i += 1
                except OSError:
                    break
    except Exception as e:
        print(f"读取注册表键 HKEY_LOCAL_MACHINE\\SOFTWARE 失败: {e}")

    return found_entries

def terminate_jiyu_processes_with_privilege(jiyu_process_infos):
    # ... (与上面相同的实现) ...
    if not jiyu_process_infos:
        print("没有要终止的极域进程。")
        return
    print("\n尝试终止极域进程...")
    for pinfo in jiyu_process_infos:
        pid = pinfo['pid']
        name = pinfo['name']
        try:
            proc = psutil.Process(pid)
            proc.terminate()
            print(f"  已发送终止信号给进程 {name} (PID: {pid})")
            time.sleep(0.1)
            if proc.is_running():
                proc.kill()
                print(f"  强制终止进程 {name} (PID: {pid}) 成功！")
            else:
                print(f"  进程 {name} (PID: {pid}) 已终止。")
        except psutil.NoSuchProcess:
            print(f"  进程 {name} (PID: {pid}) 不存在或已终止。")
        except psutil.AccessDenied:
            print(f"  拒绝访问：无法终止进程 {name} (PID: {pid})。尝试使用 taskkill。")
            try:
                subprocess.run(['taskkill', '/F', '/PID', str(pid)], check=True, capture_output=True, text=True, encoding='gbk')
                print(f"  通过 taskkill 强制终止进程 {name} (PID: {pid}) 成功！")
            except subprocess.CalledProcessError as e:
                print(f"  使用 taskkill 失败: {e.stderr.strip()}")
            except FileNotFoundError:
                print("  taskkill 命令未找到。")
        except Exception as e:
            print(f"  终止进程 {name} (PID: {pid}) 时发生错误: {e}")

def disable_and_stop_jiyu_services(jiyu_service_infos):
    # ... (与上面相同的实现) ...
    if not jiyu_service_infos:
        print("没有要停止和禁用的极域服务。")
        return
    print("\n尝试停止并禁用极域服务...")
    for svc in jiyu_service_infos:
        svc_name = svc['name']
        print(f"  正在处理服务: {svc_name}")
        try:
            print(f"    尝试停止服务 {svc_name}...")
            result = subprocess.run(['net', 'stop', svc_name], capture_output=True, text=True, check=False, encoding='gbk')
            if "服务已成功停止" in result.stdout or "服务没有启动" in result.stdout:
                print(f"    服务 {svc_name} 已停止。")
            elif "拒绝访问" in result.stderr:
                 print(f"    停止服务 {svc_name} 失败：拒绝访问。")
            else:
                print(f"    停止服务 {svc_name} 结果: {result.stdout.strip()} {result.stderr.strip()}")
        except Exception as e:
            print(f"    停止服务 {svc_name} 时发生错误: {e}")
        try:
            print(f"    尝试禁用服务 {svc_name}...")
            result = subprocess.run(['sc', 'config', svc_name, 'start=', 'disabled'], capture_output=True, text=True, check=False, encoding='gbk')
            if "SUCCESS" in result.stdout.upper():
                print(f"    服务 {svc_name} 已设置为禁用。")
            elif "拒绝访问" in result.stderr:
                 print(f"    禁用服务 {svc_name} 失败：拒绝访问。")
            else:
                print(f"    禁用服务 {svc_name} 结果: {result.stdout.strip()} {result.stderr.strip()}")
        except Exception as e:
            print(f"    禁用服务 {svc_name} 时发生错误: {e}")

def block_jiyu_network_access(jiyu_process_paths):
    # ... (与上面相同的实现) ...
    if not jiyu_process_paths:
        print("没有找到极域的可执行文件路径来设置防火墙规则。")
        return
    print("\n尝试添加防火墙规则阻止极域网络访问...")
    for app_path in set(jiyu_process_paths):
        rule_name = f"BlockJiyu_{os.path.basename(app_path).replace('.', '_')}"
        try:
            print(f"  添加出站规则 '{rule_name}' for '{app_path}'...")
            subprocess.run([
                'netsh', 'advfirewall', 'firewall', 'add', 'rule',
                'name=', rule_name, 'dir=', 'out', 'action=', 'block',
                'program=', app_path, 'enable=', 'yes'
            ], check=True, capture_output=True, text=True, encoding='gbk')
            print(f"    出站规则 '{rule_name}' 添加成功。")
        except subprocess.CalledProcessError as e:
            if "已存在" in e.stderr:
                print(f"    出站规则 '{rule_name}' 已存在。")
            else:
                print(f"    添加出站规则失败: {e.stderr.strip()}")
        except Exception as e:
            print(f"    添加出站规则时发生错误: {e}")
        try:
            print(f"  添加入站规则 '{rule_name}' for '{app_path}'...")
            subprocess.run([
                'netsh', 'advfirewall', 'firewall', 'add', 'rule',
                'name=', rule_name + "_In", 'dir=', 'in', 'action=', 'block',
                'program=', app_path, 'enable=', 'yes'
            ], check=True, capture_output=True, text=True, encoding='gbk')
            print(f"    入站规则 '{rule_name}_In' 添加成功。")
        except subprocess.CalledProcessError as e:
            if "已存在" in e.stderr:
                print(f"    入站规则 '{rule_name}_In' 已存在。")
            else:
                print(f"    添加入站规则失败: {e.stderr.strip()}")
        except Exception as e:
            print(f"    添加入站规则时发生错误: {e}")

def remove_jiyu_startup_entries(jiyu_startup_entries):
    # ... (与上面相同的实现) ...
    if not jiyu_startup_entries:
        print("没有要删除的极域启动项。")
        return
    print("\n尝试删除极域自启动项...")
    for entry_str in jiyu_startup_entries:
        key_path_name = entry_str.split(" = ")[0]
        hkey = None
        if key_path_name.startswith("HKEY_LOCAL_MACHINE"):
            hkey = winreg.HKEY_LOCAL_MACHINE
            remaining_path = key_path_name.replace("HKEY_LOCAL_MACHINE\\", "")
        elif key_path_name.startswith("HKEY_CURRENT_USER"):
            hkey = winreg.HKEY_CURRENT_USER
            remaining_path = key_path_name.replace("HKEY_CURRENT_USER\\", "")
        else:
            print(f"  无法解析启动项路径: {key_path_name}")
            continue

        try:
            last_backslash_idx = remaining_path.rfind("\\")
            subkey_path = remaining_path[:last_backslash_idx]
            name = remaining_path[last_backslash_idx + 1:]

            print(f"  正在处理注册表键: HKEY: {hkey}, Path: {subkey_path}, ValueName: {name}")
            with winreg.OpenKey(hkey, subkey_path, 0, winreg.KEY_SET_VALUE) as key:
                winreg.DeleteValue(key, name)
                print(f"  自启动项 '{name}' 已从 '{subkey_path}' 中删除。")
        except FileNotFoundError:
            print(f"  注册表键或值不存在: {key_path_name}\\{name}。")
        except PermissionError:
            print(f"  删除注册表值 '{name}' 失败：权限不足。")
        except Exception as e:
            print(f"  删除注册表值时发生错误: {e}")

def tamper_jiyu_files(jiyu_paths):
    # ... (与上面相同的实现) ...
    if not jiyu_paths:
        print("没有找到极域的文件路径来篡改。")
        return
    print("\n尝试篡改极域核心文件 (高风险操作！)...")
    for file_path in set(jiyu_paths):
        if not os.path.exists(file_path):
            print(f"  文件不存在: {file_path}")
            continue
        backup_path = file_path + ".bak"
        try:
            print(f"  尝试重命名文件 '{file_path}' 到 '{backup_path}'...")
            os.rename(file_path, backup_path)
            print(f"  文件 '{file_path}' 已重命名。")
        except PermissionError:
            print(f"  重命名文件 '{file_path}' 失败：权限不足或文件被占用。")
            print("    尝试杀死相关进程后重试，或在安全模式下操作。")
        except Exception as e:
            print(f"  重命名文件 '{file_path}' 时发生错误: {e}")

def clean_up_self_traces(script_path):
    print(f"\n尝试自毁脚本文件: {script_path}")
    try:
        os.remove(script_path)
        print(f"脚本文件 '{script_path}' 已删除。")
    except Exception as e:
        print(f"自毁失败: {e}。可能文件正在被占用，或没有权限。")

# ==================== 主控脚本逻辑 ====================
if __name__ == "__main__":
    print("--------------------------------------------------")
    print("   极域解放计划：数字反抗军启动中...   ")
    print("--------------------------------------------------")

    # 1. 权限检查与提升
    run_as_admin() # 如果不是管理员，会尝试重启脚本并退出当前实例
    if not is_admin():
        print("错误：未能获取管理员权限。大部分操作将无法执行。请手动以管理员身份运行。")
        sys.exit(1)
    else:
        print("已获取管理员权限，开始执行任务。")

    # 2. 侦察阶段
    print("\n[阶段1: 数字侦察 - 寻找敌踪]")
    jiyu_procs = find_jiyu_processes()
    jiyu_svcs = find_jiyu_services()
    jiyu_reg_entries = find_jiyu_registry_entries()

    # 收集所有可执行文件路径，用于后续的防火墙和文件篡改
    jiyu_exe_paths = [p['exe'] for p in jiyu_procs if p['exe']]
    jiyu_service_binary_paths = [s['binary_path'] for s in jiyu_svcs if s['binary_path']]
    all_jiyu_files_to_tamper = list(set(jiyu_exe_paths + jiyu_service_binary_paths))
    
    if not (jiyu_procs or jiyu_svcs or jiyu_reg_entries):
        print("\n未发现任何极域相关踪迹。可能系统未安装极域，或其隐藏方式超出本脚本侦察范围。")
        print("解放任务暂停。")
        # 可以选择自毁或退出
        clean_up_self_traces(os.path.abspath(__file__))
        sys.exit(0)

    print("\n侦察报告：")
    print(f"  发现进程数: {len(jiyu_procs)}")
    print(f"  发现服务数: {len(jiyu_svcs)}")
    print(f"  发现注册表项数: {len(jiyu_reg_entries)}")
    time.sleep(2) # 稍作停顿，让信息显示完整

    # 3. 核心打击阶段
    print("\n[阶段2: 核心打击 - 斩断敌军神经与血管]")
    
    # 优先停止服务，因为服务可能会重启进程
    disable_and_stop_jiyu_services(jiyu_svcs)
    time.sleep(3) # 等待服务停止
    
    # 再次查找进程，确保服务停止后新的进程没有被拉起
    jiyu_procs_after_svc_stop = find_jiyu_processes()
    terminate_jiyu_processes_with_privilege(jiyu_procs_after_svc_stop)
    time.sleep(2) # 等待进程终止

    # 切断网络，防止即使存活的进程也能通信
    block_jiyu_network_access(all_jiyu_files_to_tamper)
    time.sleep(1)

    # 4. 深度渗透阶段
    print("\n[阶段3: 深度渗透 - 釜底抽薪与痕迹抹除]")
    remove_jiyu_startup_entries(jiyu_reg_entries) # 删除启动项
    
    # 最后尝试篡改文件，因为这可能是最危险且需要解除锁定的
    # 注意：此操作应谨慎，可能导致系统无法正常启动或极域彻底损坏。
    # 仅作为理论上的终极手段。
    # tamper_jiyu_files(all_jiyu_files_to_tamper)
    print("\n注意：文件篡改功能已被注释，因为它风险极高，可能导致系统问题。")
    print("  如果你确定要执行，请解除代码注释，并承担可能的一切后果。")
    time.sleep(2)

    print("\n--------------------------------------------------")
    print("   极域解放任务完成！电脑已暂时从数字束缚中解放。   ")
    print("--------------------------------------------------")
    print("请注意：极域可能具有更强的自恢复能力，或在系统更新后重装。")
    print("此脚本仅代表一次成功的尝试，持续的自由需要你持续的警惕和升级你的战术。")
    print("祝你在数字世界中自由驰骋！")

    # 5. 自毁脚本 (可选，确保万无一失)
    # clean_up_self_traces(os.path.abspath(__file__))
