document.addEventListener('DOMContentLoaded', () => {
  const container = document.querySelector('.kanban-page');
  let taskId, sourceStatusId;

  container.addEventListener('dragstart', e => {
    const card = e.target.closest('.kanban-task-card');
    taskId = card.dataset.taskId;
    sourceStatusId = card.dataset.statusId;
    e.dataTransfer.effectAllowed = 'move';
  });

  container.addEventListener('dragover', e => {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
  });

  container.addEventListener('drop', e => {
    e.preventDefault();
    const targetColumn = e.target.closest('.kanban-column');
    const newStatusId = targetColumn.dataset.statusId;
    if (sourceStatusId === newStatusId) return;

    const card = document.querySelector(`.kanban-task-card[data-task-id="${taskId}"]`);
    targetColumn.querySelector('.kanban-task-list').appendChild(card);
    card.dataset.statusId = newStatusId;

    fetch(`/api/task/${taskId}/update-status/`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': document.cookie.match(/(^|;)\s*csrftoken\s*=\s*([^;]+)/)[2]
      },
      body: JSON.stringify({ status: newStatusId })
    });
  });
});