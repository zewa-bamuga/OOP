'use client'

import { useMutation } from '@tanstack/react-query'
import { useState } from 'react'
import { useForm } from 'react-hook-form'

import { Clip } from '@/types/clips.types'
import { News } from '@/types/news.types'
import { Project } from '@/types/project.types'

import { projectService } from '@/services/admin.service'

export function Admin() {
	const [activeTab, setActiveTab] = useState<
		'create' | 'projects' | 'news' | 'clips' | 'staff' | 'users'
	>('create')
	const [newsId, setNewsId] = useState<number | null>(null)
	const [newsDetails, setNewsDetails] = useState<News | null>(null)
	const [newsList, setNewsList] = useState<News[]>([])
	const [projectId, setProjectId] = useState<number | null>(null)
	const [projectDetails, setProjectDetails] = useState<Project | null>(null)
	const [projectList, setProjectList] = useState<Project[]>([])
	const [clipList, setClipList] = useState<Clip[]>([])
	const [clipId, setClipId] = useState<number | null>(null)
	const [clipDetails, setClipDetails] = useState<Clip | null>(null)
	const [staffList, setStaffList] = useState<Staff[]>([]) // Список сотрудников
	const [staffId, setStaffId] = useState<number | null>(null)
	const [staffDetails, setStaffDetails] = useState<Staff | null>(null)

	// useForm для проекта
	const {
		register: registerProject,
		handleSubmit: handleSubmitProject,
		reset: resetProject
	} = useForm({
		defaultValues: {
			name: '',
			startDate: '',
			endDate: '',
			description: '',
			participants: 0,
			lessons: 0
		}
	})

	const [userList, setUserList] = useState<User[]>([]) // Список пользователей
	const [userIdToDelete, setUserIdToDelete] = useState<number | null>(null)

	// useForm для добавления сотрудника
	const {
		register: registerStaff,
		handleSubmit: handleSubmitStaff,
		reset: resetStaff
	} = useForm({
		defaultValues: {
			projectId: '',
			staffId: ''
		}
	})

	// useForm для новостей
	const {
		register: registerNews,
		handleSubmit: handleSubmitNews,
		reset: resetNews
	} = useForm({
		defaultValues: {
			name: '',
			date: '',
			description: ''
		}
	})

	// useForm для клипов
	const {
		register: registerClip,
		handleSubmit: handleSubmitClip,
		reset: resetClip
	} = useForm({
		defaultValues: {
			name: '',
			date: new Date().toISOString().slice(0, 16),
			description: ''
		}
	})

	// Функции для работы с клипами
	const fetchClipById = async (id: number) => {
		const token = localStorage.getItem('token')
		try {
			const data = await projectService.getClipById(token, id)
			setClipDetails(data)
		} catch (error) {
			alert(
				`Error fetching clip: ${error.response?.data?.message || 'Unknown error'}`
			)
		}
	}

	const createClipMutation = useMutation({
		mutationFn: (data: any) => {
			const token = localStorage.getItem('token')
			return projectService.createClip(token, data)
		},
		onSuccess() {
			resetClip()
			alert('Clip created successfully')
		},
		onError(error: any) {
			alert(
				`Error creating clip: ${error.response?.data?.message || 'Unknown error'}`
			)
		}
	})

	const fetchAllClips = async () => {
		const token = localStorage.getItem('token')
		try {
			const response = await projectService.getClips(token)
			setClipList(response.items)
		} catch (error) {
			alert(
				`Error fetching clips: ${error.response?.data?.message || 'Unknown error'}`
			)
		}
	}

	const onSubmitClip = (data: any) => {
		createClipMutation.mutate(data)
	}

	// Функции для работы с проектами
	const fetchProjectById = async (id: number) => {
		const token = localStorage.getItem('token')
		try {
			const data = await projectService.getProjectById(token, id)
			setProjectDetails(data)
		} catch (error) {
			alert(
				`Error fetching project: ${error.response?.data?.message || 'Unknown error'}`
			)
		}
	}

	const fetchProjects = async () => {
		const token = localStorage.getItem('token')
		try {
			const response = await projectService.getProjects(token)
			setProjectList(response.items)
		} catch (error) {
			alert(
				`Error fetching projects: ${error.response?.data?.message || 'Unknown error'}`
			)
		}
	}

	const onSubmitProject = (data: any) => {
		alert(`Project submitted: ${JSON.stringify(data)}`)
		// Логика для создания проекта (не указана в исходном коде)
	}

	// Функции для работы с новостями
	const fetchNewsById = async (id: number) => {
		const token = localStorage.getItem('token')
		try {
			const data = await projectService.getNewsById(token, id)
			setNewsDetails(data)
		} catch (error) {
			alert(
				`Error fetching news: ${error.response?.data?.message || 'Unknown error'}`
			)
		}
	}

	const fetchAllStaff = async () => {
		const token = localStorage.getItem('token')
		try {
			const response = await staffService.getStaff(token)
			setStaffList(response.items)
		} catch (error) {
			alert(
				`Error fetching staff: ${error.response?.data?.message || 'Unknown error'}`
			)
		}
	}
	const createStaffMutation = useMutation({
		mutationFn: (data: any) => {
			const token = localStorage.getItem('token')
			return staffService.createStaff(token, data)
		},
		onSuccess() {
			resetStaff()
			alert('Staff member created successfully')
			fetchAllStaff() // Обновляем список после добавления
		},
		onError(error: any) {
			alert(
				`Error creating staff: ${error.response?.data?.message || 'Unknown error'}`
			)
		}
	})

	const deleteStaff = async (id: number) => {
		const token = localStorage.getItem('token')
		try {
			await staffService.deleteStaff(token, id)
			alert('Staff member deleted successfully')
			fetchAllStaff() // Обновляем список после удаления
		} catch (error) {
			alert(
				`Error deleting staff: ${error.response?.data?.message || 'Unknown error'}`
			)
		}
	}
	const onSubmitStaff = (data: any) => {
		createStaffMutation.mutate(data)
	}

	const fetchAllNews = async () => {
		const token = localStorage.getItem('token')
		try {
			const response = await projectService.getAllNews(token)
			setNewsList(response.items)
		} catch (error) {
			alert(
				`Error fetching news: ${error.response?.data?.message || 'Unknown error'}`
			)
		}
	}

	const onSubmitNews = (data: any) => {
		alert(`News submitted: ${JSON.stringify(data)}`)
		// Логика для создания новости (не указана в исходном коде)
	}

	const fetchAllUsers = async () => {
		const token = localStorage.getItem('token')
		try {
			const response = await userService.getUsers(token)
			setUserList(response.items)
		} catch (error) {
			alert(
				`Error fetching users: ${error.response?.data?.message || 'Unknown error'}`
			)
		}
	}

	const {
		register: registerUser,
		handleSubmit: handleSubmitUser,
		reset: resetUser
	} = useForm({
		defaultValues: {
			name: '',
			email: '',
			role: ''
		}
	})

	const deleteUser = async (id: number) => {
		const token = localStorage.getItem('token')
		try {
			await userService.deleteUser(token, id)
			alert('User deleted successfully')
			fetchAllUsers() // Обновляем список после удаления
		} catch (error) {
			alert(
				`Error deleting user: ${error.response?.data?.message || 'Unknown error'}`
			)
		}
	}
	const onSubmitUser = (data: any) => {
		// Логика для создания пользователя (не указана в исходном коде)
	}

	return (
		<div className='text-oopblack p-4'>
			<h1>Администрация</h1>
			<nav className='mb-4'>
				<button
					className='btn'
					onClick={() => setActiveTab('create')}
				>
					Создание проекта
				</button>
				<button
					className='btn ml-7'
					onClick={() => setActiveTab('projects')}
				>
					Проекты
				</button>
				<button
					className='btn ml-7'
					onClick={() => setActiveTab('news')}
				>
					Новости
				</button>
				<button
					className='btn ml-7'
					onClick={() => setActiveTab('clips')}
				>
					Клипы
				</button>
				<button
					className='btn ml-7'
					onClick={() => setActiveTab('staff')}
				>
					Сотрудники
				</button>
				<button
					className='btn ml-7'
					onClick={() => setActiveTab('users')}
				>
					Пользователи
				</button>
			</nav>

			{activeTab === 'create' && (
				<div className='border p-4 mb-4 rounded shadow'>
					<h2>Создание проекта</h2>
					<form onSubmit={handleSubmitProject(onSubmitProject)}>
						{/* Форма создания проекта */}
						<div className='mb-3'>
							<label>Название проекта</label>
							<input
								{...registerProject('name')}
								placeholder='Project name'
								required
								className='form-input'
							/>
						</div>
						<div className='mb-3'>
							<label>Дата начала</label>
							<input
								{...registerProject('startDate')}
								type='datetime-local'
								required
								className='form-input'
							/>
						</div>
						<div className='mb-3'>
							<label>Дата окончания</label>
							<input
								{...registerProject('endDate')}
								type='datetime-local'
								required
								className='form-input'
							/>
						</div>
						<div className='mb-3'>
							<label>Описание</label>
							<textarea
								{...registerProject('description')}
								placeholder='Description'
								className='form-input'
							/>
						</div>
						<div className='mb-3'>
							<label>Количество участников</label>
							<input
								{...registerProject('participants')}
								type='number'
								placeholder='Participants'
								required
								className='form-input'
							/>
						</div>
						<div className='mb-3'>
							<label>Количество уроков</label>
							<input
								{...registerProject('lessons')}
								type='number'
								placeholder='Lessons'
								required
								className='form-input'
							/>
						</div>
						<button
							type='submit'
							className='btn'
						>
							Создать проект
						</button>
					</form>

					<h2 className='mt-4'>Добавление сотрудника в проект</h2>
					<form
						onSubmit={handleSubmitStaff(data =>
							alert(`Staff added to project: ${JSON.stringify(data)}`)
						)}
					>
						{/* Форма добавления сотрудника */}
						<div className='mb-3'>
							<label>ID проекта</label>
							<input
								{...registerStaff('projectId')}
								type='number'
								placeholder='Project ID'
								required
								className='form-input'
							/>
						</div>
						<div className='mb-3'>
							<label>ID сотрудника</label>
							<input
								{...registerStaff('staffId')}
								placeholder='Staff ID'
								required
								className='form-input'
							/>
						</div>
						<button
							type='submit'
							className='btn'
						>
							Добавить сотрудника
						</button>
					</form>
				</div>
			)}

			{activeTab === 'projects' && (
				<div className='border p-4 rounded shadow'>
					<h2>Вывод всех проектов</h2>
					<button
						onClick={fetchProjects}
						className='btn'
					>
						Вывести все проекты
					</button>
					<div className='mt-4'>
						<input
							type='number'
							value={projectId || ''}
							onChange={e => setProjectId(Number(e.target.value))}
							placeholder='Введите ID проекта'
							className='form-input'
						/>
						<button
							onClick={() => projectId && fetchProjectById(projectId)}
							className='btn'
						>
							Получить проект
						</button>
					</div>
					{projectDetails && (
						<div className='mt-4 border p-2 rounded'>
							<h3>{projectDetails.name}</h3>
							<p>Описание: {projectDetails.description}</p>
							<p>
								Дата начала:{' '}
								{new Date(projectDetails.startDate).toLocaleString()}
							</p>
							<p>
								Дата окончания:{' '}
								{new Date(projectDetails.endDate).toLocaleString()}
							</p>
							<p>Участники: {projectDetails.participants}</p>
							<p>Уроки: {projectDetails.lessons}</p>
							<p>Лайки: {projectDetails.likes}</p>
						</div>
					)}
					<ul className='mt-4'>
						{projectList.map((project: Project) => (
							<li
								key={project.id}
								className='mb-2 border p-2 rounded'
							>
								<h3>{project.name}</h3>
								<p>Описание: {project.description}</p>
								<p>
									Дата начала: {new Date(project.startDate).toLocaleString()}
								</p>
								<p>
									Дата окончания: {new Date(project.endDate).toLocaleString()}
								</p>
								<p>Участники: {project.participants}</p>
								<p>Уроки: {project.lessons}</p>
								<p>Лайки: {project.likes}</p>
							</li>
						))}
					</ul>
				</div>
			)}

			{activeTab === 'news' && (
				<div className='border p-4 rounded shadow'>
					<h2>Создание новости</h2>
					<form onSubmit={handleSubmitNews(onSubmitNews)}>
						<div className='mb-3'>
							<label>Название новости</label>
							<input
								{...registerNews('name')}
								placeholder='News name'
								required
								className='form-input'
							/>
						</div>
						<div className='mb-3'>
							<label>Дата</label>
							<input
								{...registerNews('date')}
								type='datetime-local'
								required
								className='form-input'
							/>
						</div>
						<div className='mb-3'>
							<label>Описание</label>
							<textarea
								{...registerNews('description')}
								placeholder='Description'
								className='form-input'
							/>
						</div>
						<button
							type='submit'
							className='btn'
						>
							Создать новость
						</button>
					</form>

					<h2 className='mt-4'>Все новости</h2>
					<button
						onClick={fetchAllNews}
						className='btn'
					>
						Получить все новости
					</button>
					<ul className='mt-4'>
						{newsList.map(news => (
							<li
								key={news.id}
								className='mb-2 border p-2 rounded'
							>
								<h3>{news.name}</h3>
								<p>Дата: {new Date(news.date).toLocaleString()}</p>
								<p>Описание: {news.description}</p>
							</li>
						))}
					</ul>

					<h2 className='mt-4'>Получение новости по ID</h2>
					<input
						type='number'
						value={newsId || ''}
						onChange={e => setNewsId(Number(e.target.value))}
						placeholder='Введите ID новости'
						className='form-input'
					/>
					<button
						onClick={() => newsId && fetchNewsById(newsId)}
						className='btn'
					>
						Получить новость
					</button>

					{newsDetails && (
						<div className='mt-4 border p-2 rounded'>
							<h3>{newsDetails.name}</h3>
							<p>Дата: {new Date(newsDetails.date).toLocaleString()}</p>
							<p>Описание: {newsDetails.description}</p>
						</div>
					)}
				</div>
			)}

			{activeTab === 'clips' && (
				<div className='border p-4 rounded shadow'>
					<h2>Создание клипа</h2>
					<form onSubmit={handleSubmitClip(onSubmitClip)}>
						<div className='mb-3'>
							<label>Название клипа</label>
							<input
								{...registerClip('name')}
								placeholder='Clip name'
								required
								className='form-input'
							/>
						</div>
						<div className='mb-3'>
							<label>Дата</label>
							<input
								{...registerClip('date')}
								type='datetime-local'
								required
								className='form-input'
							/>
						</div>
						<div className='mb-3'>
							<label>Описание</label>
							<textarea
								{...registerClip('description')}
								placeholder='Description'
								className='form-input'
							/>
						</div>
						<button
							type='submit'
							className='btn'
						>
							Создать клип
						</button>
					</form>

					<h2 className='mt-4'>Все клипы</h2>
					<button
						onClick={fetchAllClips}
						className='btn'
					>
						Получить все клипы
					</button>
					<ul className='mt-4'>
						{clipList.map(clip => (
							<li
								key={clip.id}
								className='mb-2 border p-2 rounded'
							>
								<h3>{clip.name}</h3>
								<p>Дата: {new Date(clip.date).toLocaleString()}</p>
								<p>Описание: {clip.description}</p>
							</li>
						))}
					</ul>

					<h2 className='mt-4'>Получение клипа по ID</h2>
					<input
						type='number'
						value={clipId || ''}
						onChange={e => setClipId(Number(e.target.value))}
						placeholder='Введите ID клипа'
						className='form-input'
					/>
					<button
						onClick={() => clipId && fetchClipById(clipId)}
						className='btn'
					>
						Получить клип
					</button>

					{clipDetails && (
						<div className='mt-4 border p-2 rounded'>
							<h3>{clipDetails.name}</h3>
							<p>Дата: {new Date(clipDetails.date).toLocaleString()}</p>
							<p>Описание: {clipDetails.description}</p>
						</div>
					)}
				</div>
			)}

			{activeTab === 'staff' && (
				<div className='border p-4 rounded shadow'>
					<h2>Создание сотрудника</h2>
					<form onSubmit={handleSubmitStaff(onSubmitStaff)}>
						<div className='mb-3'>
							<label>Имя</label>
							<input
								{...registerStaff('firstname')}
								placeholder='Имя'
								required
								className='form-input'
							/>
						</div>
						<div className='mb-3'>
							<label>Фамилия</label>
							<input
								{...registerStaff('lastname')}
								placeholder='Фамилия'
								required
								className='form-input'
							/>
						</div>
						<div className='mb-3'>
							<label>Квалификация</label>
							<input
								{...registerStaff('qualification')}
								placeholder='Квалификация'
								required
								className='form-input'
							/>
						</div>
						<div className='mb-3'>
							<label>Должность</label>
							<input
								{...registerStaff('post')}
								placeholder='Должность'
								required
								className='form-input'
							/>
						</div>
						<div className='mb-3'>
							<label>Email</label>
							<input
								{...registerStaff('email')}
								type='email'
								placeholder='Email'
								required
								className='form-input'
							/>
						</div>
						<div className='mb-3'>
							<label>Ссылка на VK</label>
							<input
								{...registerStaff('linkToVk')}
								placeholder='Ссылка на VK'
								className='form-input'
							/>
						</div>
						<button
							type='submit'
							className='btn'
						>
							Создать сотрудника
						</button>
					</form>

					<h2 className='mt-4'>Все сотрудники</h2>
					<button
						onClick={fetchAllStaff}
						className='btn'
					>
						Получить всех сотрудников
					</button>
					<ul className='mt-4'>
						{staffList.map(staff => (
							<li
								key={staff.id}
								className='mb-2 border p-2 rounded'
							>
								<h3>
									{staff.firstname} {staff.lastname}
								</h3>
								<p>Квалификация: {staff.qualification}</p>
								<p>Должность: {staff.post}</p>
								<p>Email: {staff.email}</p>
								<p>
									<a
										href={staff.linkToVk}
										target='_blank'
										rel='noopener noreferrer'
									>
										VK
									</a>
								</p>
								<button
									onClick={() => deleteStaff(staff.id)}
									className='btn'
								>
									Удалить сотрудника
								</button>
							</li>
						))}
					</ul>
				</div>
			)}

			{activeTab === 'users' && (
				<div className='border p-4 rounded shadow'>
					<h2>Вывод всех пользователей</h2>
					<button
						onClick={fetchAllUsers}
						className='btn'
					>
						Получить всех пользователей
					</button>
					<ul className='mt-4'>
						{userList.map(user => (
							<li
								key={user.id}
								className='mb-2 border p-2 rounded'
							>
								<h3>{user.name}</h3>
								<p>Email: {user.email}</p>
								<p>Роль: {user.role}</p>
								<button
									className='btn'
									onClick={() => {
										setUserIdToDelete(user.id)
										deleteUser(user.id)
									}}
								>
									Удалить
								</button>
							</li>
						))}
					</ul>
					<input
						type='number'
						value={userIdToDelete || ''}
						onChange={e => setUserIdToDelete(Number(e.target.value))}
						placeholder='Введите ID пользователя для удаления'
						className='form-input'
					/>
					<button
						onClick={() => userIdToDelete && deleteUser(userIdToDelete)}
						className='btn'
					>
						Удалить пользователя
					</button>
				</div>
			)}
		</div>
	)
}
