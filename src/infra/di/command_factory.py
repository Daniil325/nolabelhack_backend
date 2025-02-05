from dishka import Provider, Scope, provide

from src.usecases.vote import CreateVoteCommand, DeleteVoteCommand, UpdateVoteCommand
from src.usecases.answers import CreateAnswerCommand, DeleteAnswerCommand, UpdateAnswerCommand


class CommandProvider(Provider):
    scope = Scope.REQUEST
    
    create_answer_command = provide(CreateAnswerCommand)
    update_answer_command = provide(UpdateAnswerCommand)
    delete_answer_command = provide(DeleteAnswerCommand)
    
    create_vote_command = provide(CreateVoteCommand)
    update_vote_command = provide(UpdateVoteCommand)
    delete_vote_command = provide(DeleteVoteCommand)
    