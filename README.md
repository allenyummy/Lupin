# Lupin

Lupin is a project to help people to register to see a famous doctor.

I assume that socioeconomic status of target consumers to Lupin service are higher than that of usual people; therefore, I figure out a business model that I charge these people when they ask me to help them register to see a famous doctor, and ask them what percentage of total charge they're willing to donate to disadvantaged groups. Once their registration is confirmed, I'll charge them and return a donation receipt to ensure their money is actually donated to disadvantaged groups.

I believe that Lupin service excludes the rights of disadvantaged groups to see a doctor; however, I saw this kind of service have already existed on the Internet and they charge a lot. I try to make it right. This is the main purpose of Lupin project.

Why Lupin ? Lupin is a guy that always rob the rich to help the poor. I think maybe his spirit is similar to this project (Correct me if I'm wrong). If not, I hope he is a guy I would like to be.

---

## [台大醫院網路掛號](https://reg.ntuh.gov.tw/WebAdministration/)

1. Init webdriver (chrome, edge, firefox, safari)
    + 自行下載、分層存放並記錄版本
    
2. Get entrance of webpage
    + 前往 f"https://reg.ntuh.gov.tw/webadministration/DoctorServiceQueryByDrName.aspx?HospCode=T0&QueryName={醫生姓名}
    + 收集有名醫生的 webpage，可以去蝦皮找
    + 目前狀況可能還不需要寫連點程式，只需有好的網路，並在好的時間點開啟程式。

3. Click the correct 掛號 button
    + 點選表格內的正確地掛號鈕，須考慮時間、已掛號、停止掛號等狀況。
    + 值得注意的是網頁通常呈現兩個禮拜的掛號狀況，掛號鈕的 Xpath 具有可預測性。
    + 點選此頁之後會跳轉，考慮是否要停頓一下。

4. Send information
    + 身分證字號，由使用者提供
        + 個資不要 push 上去
    + 勾選證件類別，開發者自行預設為身分證字號
    + 出生年月日，由使用者提供
        + 個資不要 push 上去
    + 驗證碼，開發者使用驗證碼破解器處理 
        + 記得把驗證碼與破解後的東西儲存起來，當作資料集
        + API key 不要 push 上去 repo

5. Submit
