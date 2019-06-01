# comfort_transport
オープンデータコンテストに向けたwebアプリ開発

## git運用について
git-flowの運用を想定しています。

### ブランチ
master: リリースしたもの  
develop: 開発用  
feature/content: 何か新しい機能を追加する場合  
hotfix/content : バグ修正  
release/content: リリース用  
※ブランチを作る時にcontentのところは内容を書いてください  

developブランチにマージする時にPull Requestを出してレビューする運用都する予定  

### AWS
webアプリケーションの公開先としてAWS E2サーバーを利用
- Public DNS: ec2-18-191-220-156.us-east-2.compute.amazonaws.com
- Public IP: 18.191.220.156
- Private DNS: ip-172-31-20-105.us-east-2.compute.internal
- Private IP: 172.31.20.105
- Port: 5000
