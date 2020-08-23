from aiogram.utils.helper import Helper, HelperMode, ListItem
from aiogram.dispatcher import FSMContext
from tasklist import TaskStage

from pprint import pprint

# States
class Phase(Helper):
    mode = HelperMode.snake_case

    IDEAS = ListItem()
    TASKS = ListItem()
    ARCHIVE = ListItem()
    EDIT_IDEA = ListItem()
    EDIT_TASK = ListItem()
    EDIT_ARCH = ListItem()

    def get(stage):
    #  trick to avoid sorted items problem that Helper does alphabetically
        return Phase.all()[(stage.value + 4) % 6]

    async def get_stage(state: FSMContext):
        stage = TaskStage.TODO
        cur_state = await state.get_state()
        pprint(cur_state)
        if Phase.EDIT_IDEA[0] in cur_state or Phase.IDEAS[0] in cur_state:
            stage = TaskStage.IDEA
        elif Phase.EDIT_ARCH[0] in cur_state or Phase.ARCHIVE[0] in cur_state:
            stage = TaskStage.DONE

        return stage

