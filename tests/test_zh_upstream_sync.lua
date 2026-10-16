local T=require("tests.testlib")
local bootstrap=require("tests.bootstrap")
bootstrap.load()
dofile("main.lua")
local suite=T.suite()
suite.test("2.0.4 game-over A callback continues only after the slide",function()
    local g=bootstrap.new_game(736);G=g;g.STATE=g.STATES.GAME_OVER
    local count=0;g.continue_from_game_over=function() count=count+1 end
    g.scene_transition_active=function() return false end
    love.gamepadpressed(nil,"a");T.assert_eq(count,1)
    g.scene_transition_active=function() return true end
    love.gamepadpressed(nil,"a");T.assert_eq(count,1)
end)
suite.test("2.0.4 modal deck view blocks underlying card tooltips",function()
    local g=bootstrap.new_game(737);G=g;g.STATE=g.STATES.SHOP
    local count=0;g.hand={card_nodes={{draw_tooltip_overlay=function() count=count+1 end}}}
    g.modal_overlay_open=function() return true end
    g:draw_tooltips_on_top();T.assert_eq(count,0)
end)
return suite
