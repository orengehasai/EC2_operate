# EC2_operate

Pythonの仮想環境（venvなど）で実行してください。

---

## Usage

### コマンド一覧

| コマンド      | 説明               |
| ------------- | ------------------ |
| `start`       | インスタンス開始   |
| `stop`        | インスタンス停止   |
| `terminate`   | インスタンス削除   |
| `list`        | インスタンス一覧表示 |
| `create`      | インスタンス新規作成 |

---

### create 以外のコマンドの使い方

```bash
python EC2_operate.py [start|stop|terminate|list] [instance_id1 instance_id2 ...]
