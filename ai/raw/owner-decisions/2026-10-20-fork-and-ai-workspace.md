# Fork setup and the AI knowledge workspace

> Source: maintainer (GitHub x484838830) in chat with Claude Code
> Collected: 2026-10-20
> Published: 2026-10-20

The maintainer's own words are quoted in Chinese. The English lines record what was done in response. Nothing else is added.

## Request 1 — work on a copy, not on the live platform

> 這個github，若要修改分析平台，在不影響現有平台的運作下，請問你可以複製一份，在他處修改新增功能嗎？可以的話請幫我複製github，clone到我桌面資料夾中。

Done: the repository charleslin2003-prog/Exercise_Evaluation was cloned to the folder Exercise_Evaluation on the maintainer's Desktop. [removed: absolute path, 2026-10-22, SCHEMA.md §9]

## Request 2 — fork to the maintainer's account

> 好。用一個到我帳號，命命成：frokcharleslin2003-prog_Exercise_Evaluation

Claude asked whether "frok" was a typo. The maintainer chose: forkcharleslin2003-prog_Exercise_Evaluation.

Done: GitHub fork x484838830/forkcharleslin2003-prog_Exercise_Evaluation, with all four branches (master, dev, chart-handoff, 一版).

Local remotes after setup:

- origin = the fork. Pushes go here.
- upstream = the original repository. Its push URL is set to DISABLED-do-not-push-to-production, so a push to upstream fails.
- remote.pushDefault = origin, push.autoSetupRemote = true.

## Request 3 — push with GitHub Desktop

> 也幫我設定好push，到時候我用github Desktop可以直接更新上去

Done: the checkout was added to GitHub Desktop. The maintainer confirmed: 可以囉

## Request 4 — the AI knowledge and work area

> 然後請你再這資料夾中建立一個AI知識與工作區。
> 裡面你用：https://github.com/Astro-Han/karpathy-llm-wiki ，這種方法，來建立知識。然後知識要打造可維護，可更新的方式，因為你每次不可能全部掃描過全部檔案，看有沒有更新。
> 然後裡面打造資料的整理資料的方式可以參考：https://github.com/danyuchn/asd-ste100-skill
> 這樣才不會搞錯。

## Decisions on the questions Claude asked (2026-10-20)

Language of the wiki:

> 你可以用英文沒關係，反正到時候這個應該都會是你在看，我只是怕你做到後面會搞混。

Push ai/ to the fork: yes (option 推上去).

Scope of the first round:

> 整個專案 評核頁、後端、部署、分析平台全部整理，第一輪會花比較久
> 然後除了程式之外，還要知道他的目的、知識領域等等。
