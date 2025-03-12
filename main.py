from astrbot.api.all import *

@register("hearthstone_decks", "Your Name", "炉石传说卡组插件", "1.0.0")
class HearthstoneDecksPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @command("炉石卡组")
    async def hearthstone_decks(self, event: AstrMessageEvent):
        '''获取炉石传说萨满卡组信息'''
        try:
            import hsdata

            # 获取卡组数据
            decks = hsdata.HSBoxDecks()
            # 若未找到本地数据，会自动从网络获取
            print('从炉石盒子获取到', len(decks), '个卡组数据！')

            # 检查是否获取到卡组数据
            if len(decks) == 0:
                yield event.plain_result("未获取到任何卡组数据，请检查网络连接或稍后再试。")
                return

            # 更新卡组数据
            # decks.update()

            # 调整搜索条件
            found = decks.search(
                career='萨满',
                mode=hsdata.MODE_STANDARD,
                min_games=1000,  # 调整为较低的对战场次要求
                win_rate_top_n=5)
            print('其中5个胜率最高的萨满卡组:')
            result_str = ""
            if not found:
                result_str = "未找到符合条件的萨满卡组。"
            else:
                for deck in found:
                    result_str += '{}: {} 场, {:.2%} 胜\n'.format(
                        deck.name, deck.games, deck.win_rate)

                # 查看卡组中的卡牌
                print('其中第一个卡组用了这些卡牌')
                print(found[0].cards)
                result_str += "\n第一个卡组的卡牌:\n" + str(found[0].cards)

            yield event.plain_result(result_str)

        except Exception as e:
            yield event.plain_result(f"获取卡组信息时出错: {str(e)}")
